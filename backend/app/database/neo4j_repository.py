import logging
from typing import Optional, Dict, Any
from app.database.interfaces import BaseProjectRepository
from app.database.neo4j_connection import neo4j_conn
from app.models.onboarding_model import OnboardingModel

logger = logging.getLogger("gcip-neo4j-repository")

class Neo4jProjectRepository(BaseProjectRepository):
    def __init__(self):
        # We ensure driver is initialized
        neo4j_conn.connect()
        self.driver = neo4j_conn.driver

    def save_onboarding(self, tenant_id: str, onboarding_data: OnboardingModel) -> bool:
        if not self.driver:
            logger.error("Neo4j driver is not initialized. Cannot save onboarding data.")
            return False

        try:
            with self.driver.session() as session:
                session.execute_write(self._save_project_tx, tenant_id, onboarding_data)
            logger.info(f"Successfully saved project {onboarding_data.project_id} in Neo4j.")
            return True
        except Exception as e:
            logger.error(f"Error saving project onboarding in Neo4j: {e}")
            return False

    def get_project(self, tenant_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        if not self.driver:
            logger.error("Neo4j driver is not initialized. Cannot fetch project.")
            return None

        try:
            with self.driver.session() as session:
                project_data = session.execute_read(self._get_project_tx, tenant_id, project_id)
            return project_data
        except Exception as e:
            logger.error(f"Error fetching project from Neo4j: {e}")
            return None

    @staticmethod
    def _save_project_tx(tx, tenant_id: str, onboarding_data: OnboardingModel):
        # 1. Merge/Update Project Node
        project_query = """
        MERGE (p:Project {id: $project_id, tenant_id: $tenant_id})
        SET p.name = $project_name,
            p.budget = $total_budget_usd,
            p.is_takeover = $is_takeover,
            p.historical_leakage_audit = $historical_leakage_audit,
            p.baseline_version = $baseline_version
        """
        tx.run(
            project_query,
            project_id=onboarding_data.project_id,
            tenant_id=tenant_id,
            project_name=onboarding_data.project_name,
            total_budget_usd=onboarding_data.total_budget_usd,
            is_takeover=onboarding_data.is_takeover,
            historical_leakage_audit=onboarding_data.historical_leakage_audit,
            baseline_version=onboarding_data.baseline_version
        )

        # 2. Add BOQ Items if any exist
        if onboarding_data.boq_items:
            boq_query = """
            MATCH (p:Project {id: $project_id, tenant_id: $tenant_id})
            UNWIND $boq_items AS boq
            MERGE (b:BOQItem {id: boq.id, tenant_id: $tenant_id})
            SET b.poz_no = boq.poz_no,
                b.description = boq.description,
                b.quantity = boq.quantity,
                b.unit = boq.unit,
                b.unit_price = boq.unit_price,
                b.total_price = boq.total_price,
                b.discipline = boq.discipline
            MERGE (p)-[:HAS_BOQ]->(b)
            """
            # Ensure every BOQ item has a unique ID, default to generating if missing
            processed_boq = []
            for i, item in enumerate(onboarding_data.boq_items):
                boq_copy = item.copy()
                if "id" not in boq_copy:
                    boq_copy["id"] = f"{onboarding_data.project_id}-boq-{i}"
                if "discipline" not in boq_copy:
                    boq_copy["discipline"] = "CIVIL"
                processed_boq.append(boq_copy)

            tx.run(
                boq_query,
                project_id=onboarding_data.project_id,
                tenant_id=tenant_id,
                boq_items=processed_boq
            )

        # 3. Add Subcontractors and relate them via Contract
        if onboarding_data.subcontractors:
            sub_query = """
            MATCH (p:Project {id: $project_id, tenant_id: $tenant_id})
            UNWIND $subcontractors AS sub
            MERGE (s:Subcontractor {id: sub.id, tenant_id: $tenant_id})
            SET s.name = sub.name
            MERGE (c:Contract {id: sub.contract_id, tenant_id: $tenant_id})
            SET c.name = sub.contract_name
            MERGE (c)-[:BELONGS_TO]->(p)
            MERGE (s)-[:UNDER_CONTRACT]->(c)
            """
            processed_subs = []
            for i, sub in enumerate(onboarding_data.subcontractors):
                sub_copy = sub.copy()
                if "id" not in sub_copy:
                    sub_copy["id"] = f"sub-{i}"
                if "contract_id" not in sub_copy:
                    sub_copy["contract_id"] = f"contract-{onboarding_data.project_id}-{i}"
                if "contract_name" not in sub_copy:
                    sub_copy["contract_name"] = f"Contract for {sub_copy.get('name', 'Subcontractor')}"
                processed_subs.append(sub_copy)

            tx.run(
                sub_query,
                project_id=onboarding_data.project_id,
                tenant_id=tenant_id,
                subcontractors=processed_subs
            )

    @staticmethod
    def _get_project_tx(tx, tenant_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        # 1. Fetch Project
        project_query = """
        MATCH (p:Project {id: $project_id, tenant_id: $tenant_id})
        RETURN p
        """
        result = tx.run(project_query, project_id=project_id, tenant_id=tenant_id)
        record = result.single()
        if not record:
            return None

        project_node = record["p"]
        project_data = {
            "project_id": project_node.get("id"),
            "project_name": project_node.get("name", ""),
            "total_budget_usd": float(project_node["budget"]) if project_node.get("budget") is not None else 0.0,
            "is_takeover": bool(project_node["is_takeover"]) if project_node.get("is_takeover") is not None else False,
            "historical_leakage_audit": bool(project_node["historical_leakage_audit"]) if project_node.get("historical_leakage_audit") is not None else True,
            "baseline_version": project_node.get("baseline_version", "Rev0"),
            "boq_items": [],
            "subcontractors": []
        }

        # 2. Fetch BOQ Items
        boq_query = """
        MATCH (p:Project {id: $project_id, tenant_id: $tenant_id})-[:HAS_BOQ]->(b:BOQItem)
        RETURN b
        """
        boq_result = tx.run(boq_query, project_id=project_id, tenant_id=tenant_id)
        for r in boq_result:
            b_node = r["b"]
            project_data["boq_items"].append({
                "id": b_node.get("id"),
                "poz_no": b_node.get("poz_no", ""),
                "description": b_node.get("description", ""),
                "quantity": float(b_node["quantity"]) if b_node.get("quantity") is not None else 0.0,
                "unit": b_node.get("unit", ""),
                "unit_price": float(b_node["unit_price"]) if b_node.get("unit_price") is not None else 0.0,
                "total_price": float(b_node["total_price"]) if b_node.get("total_price") is not None else 0.0,
                "discipline": b_node.get("discipline", "CIVIL")
            })

        # 3. Fetch Subcontractors
        sub_query = """
        MATCH (s:Subcontractor {tenant_id: $tenant_id})-[:UNDER_CONTRACT]->(c:Contract)-[:BELONGS_TO]->(p:Project {id: $project_id, tenant_id: $tenant_id})
        RETURN s, c
        """
        sub_result = tx.run(sub_query, project_id=project_id, tenant_id=tenant_id)
        for r in sub_result:
            s_node = r["s"]
            c_node = r["c"]
            project_data["subcontractors"].append({
                "id": s_node.get("id"),
                "name": s_node.get("name", ""),
                "contract_id": c_node.get("id"),
                "contract_name": c_node.get("name", "")
            })

        return project_data

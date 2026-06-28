import logging
from typing import Optional, Dict, Any
from app.database.interfaces import BaseProjectRepository
from app.models.onboarding_model import OnboardingModel

logger = logging.getLogger("gcip-mock-repository")

class InMemoryProjectRepository(BaseProjectRepository):
    def __init__(self):
        # Nested dictionary mapping tenant_id -> {project_id: data_dict}
        self._storage: Dict[str, Dict[str, Any]] = {}

    def save_onboarding(self, tenant_id: str, onboarding_data: OnboardingModel) -> bool:
        logger.info(f"[MockDB] Saving project {onboarding_data.project_id} under Tenant: {tenant_id}")
        if tenant_id not in self._storage:
            self._storage[tenant_id] = {}
        
        # Convert onboarding data model to dict
        data_dict = onboarding_data.model_dump()
        self._storage[tenant_id][onboarding_data.project_id] = data_dict
        return True

    def get_project(self, tenant_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        logger.info(f"[MockDB] Fetching project {project_id} under Tenant: {tenant_id}")
        tenant_projects = self._storage.get(tenant_id)
        if not tenant_projects:
            return None
        return tenant_projects.get(project_id)

# Singleton instance of the mock repository
mock_project_repo = InMemoryProjectRepository()

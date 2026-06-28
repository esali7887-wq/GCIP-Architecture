import logging
from typing import List, Dict, Any
from app.database.neo4j_connection import neo4j_conn

logger = logging.getLogger("gcip-neo4j-vector")

class Neo4jVectorStore:
    def __init__(self):
        neo4j_conn.connect()
        self.driver = neo4j_conn.driver

    def initialize_vector_index(self):
        if not self.driver:
            logger.error("Neo4j driver not initialized. Cannot create vector index.")
            return

        query = """
        CREATE VECTOR INDEX gcip_chunks IF NOT EXISTS
        FOR (n:Chunk) ON (n.embedding)
        OPTIONS {indexConfig: {
          `vector.dimensions`: 768,
          `vector.similarity_function`: 'cosine'
        }}
        """
        try:
            with self.driver.session() as session:
                session.run(query)
            logger.info("Neo4j vector index 'gcip_chunks' verified/created successfully (768 dimensions).")
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j vector index: {e}")

    def store_chunk_tx(self, tx, project_id: str, tenant_id: str, chunk_id: str, text: str, embedding: List[float], source: str):
        query = """
        MATCH (p:Project {id: $project_id, tenant_id: $tenant_id})
        MERGE (c:Chunk {id: $chunk_id})
        SET c.text = $text,
            c.embedding = $embedding,
            c.source = $source
        MERGE (p)-[:HAS_DOCUMENT_CHUNK]->(c)
        """
        tx.run(
            query,
            project_id=project_id,
            tenant_id=tenant_id,
            chunk_id=chunk_id,
            text=text,
            embedding=embedding,
            source=source
        )

    def similarity_search(self, tenant_id: str, project_id: str, query_vector: List[float], k: int = 3) -> List[Dict[str, Any]]:
        if not self.driver:
            logger.error("Neo4j driver not initialized. Cannot search vectors.")
            return []

        search_query = """
        CALL db.index.vector.queryNodes('gcip_chunks', $k, $query_vector)
        YIELD node, score
        MATCH (node)<-[:HAS_DOCUMENT_CHUNK]-(p:Project {id: $project_id, tenant_id: $tenant_id})
        RETURN node.text AS text, node.source AS source, score
        """
        try:
            results = []
            with self.driver.session() as session:
                res = session.run(search_query, query_vector=query_vector, k=k, project_id=project_id, tenant_id=tenant_id)
                for r in res:
                    results.append({
                        "text": r["text"],
                        "source": r["source"],
                        "score": float(r["score"])
                    })
            return results
        except Exception as e:
            logger.error(f"Vector similarity search failed: {e}")
            return []

neo4j_vector_store = Neo4jVectorStore()

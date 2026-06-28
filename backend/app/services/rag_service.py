import logging
import uuid
from typing import List
from app.services.embedding_service import embedding_service
from app.database.neo4j_vector import neo4j_vector_store
from app.database.neo4j_connection import neo4j_conn

logger = logging.getLogger("gcip-rag-service")

class RAGService:
    def chunk_text(self, text: str, chunk_size: int = 200, chunk_overlap: int = 20) -> List[str]:
        # Recursive-like simple overlap word chunker
        if not text:
            return []
        
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunks.append(" ".join(chunk_words))
            if i + chunk_size >= len(words):
                break
            i += (chunk_size - chunk_overlap)
            
        return chunks

    def process_and_index_document(self, tenant_id: str, project_id: str, source_name: str, text: str) -> int:
        chunks = self.chunk_text(text)
        if not chunks:
            logger.warning("Empty document. No chunks generated.")
            return 0

        logger.info(f"Generated {len(chunks)} chunks for document '{source_name}'. Generating embeddings and saving...")
        
        driver = neo4j_conn.driver
        if not driver:
            logger.error("Neo4j driver is not active. Cannot save RAG chunks.")
            return 0

        try:
            with driver.session() as session:
                def _write_chunks(tx):
                    for idx, chunk in enumerate(chunks):
                        chunk_id = f"{project_id}-{source_name.replace(' ', '_')}-chunk-{idx}"
                        # Generate embedding
                        emb = embedding_service.get_embedding(chunk)
                        neo4j_vector_store.store_chunk_tx(
                            tx=tx,
                            project_id=project_id,
                            tenant_id=tenant_id,
                            chunk_id=chunk_id,
                            text=chunk,
                            embedding=emb,
                            source=source_name
                        )
                session.execute_write(_write_chunks)
            logger.info(f"Successfully indexed {len(chunks)} chunks in Neo4j vector store.")
            return len(chunks)
        except Exception as e:
            logger.error(f"Error indexing chunks in Neo4j: {e}")
            return 0

rag_service = RAGService()

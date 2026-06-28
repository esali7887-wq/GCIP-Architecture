import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.rag_model import RAGUploadModel, RAGQueryModel
from app.middlewares.tenant_validator import get_current_tenant
from app.services.rag_service import rag_service
from app.services.embedding_service import embedding_service
from app.database.neo4j_vector import neo4j_vector_store

logger = logging.getLogger("gcip-rag-router")

router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_rag_document(
    payload: RAGUploadModel,
    tenant_id: str = Depends(get_current_tenant)
):
    logger.info(f"RAG upload initiated for tenant '{tenant_id}', project '{payload.project_id}'")
    
    # Process document: chunk, embed, and index in Neo4j
    chunks_indexed = rag_service.process_and_index_document(
        tenant_id=tenant_id,
        project_id=payload.project_id,
        source_name=payload.source_name,
        text=payload.text
    )
    
    if chunks_indexed == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to index document chunks. Check server logs."
        )
        
    return {
        "status": "success",
        "message": f"Successfully chunked and indexed document '{payload.source_name}'.",
        "chunks_indexed": chunks_indexed
    }

@router.post("/query", status_code=status.HTTP_200_OK)
async def query_rag(
    payload: RAGQueryModel,
    tenant_id: str = Depends(get_current_tenant)
):
    logger.info(f"RAG query initiated for tenant '{tenant_id}', project '{payload.project_id}': '{payload.query}'")
    
    # 1. Generate search query embedding vector (768 dimensions)
    try:
        query_vector = embedding_service.get_embedding(payload.query)
    except Exception as e:
        logger.error(f"Failed to generate query embedding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate query embedding: {e}"
        )
        
    # 2. Query similarity index in Neo4j vector store
    results = neo4j_vector_store.similarity_search(
        tenant_id=tenant_id,
        project_id=payload.project_id,
        query_vector=query_vector,
        k=payload.k
    )
    
    return {
        "status": "success",
        "query": payload.query,
        "results_count": len(results),
        "results": results
    }

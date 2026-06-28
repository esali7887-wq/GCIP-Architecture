import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.neo4j_connection import neo4j_conn
from app.database.redis_client import redis_client
from app.middlewares.tenant_validator import TenantValidatorMiddleware
from app.routers.onboarding import router as onboarding_router
from app.routers.rag_router import router as rag_router
from app.database.neo4j_vector import neo4j_vector_store

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gcip-backend")

app = FastAPI(
    title="Global Construction Intelligence Platform (GCIP)",
    description="Deterministic AI & progress payment system for AEC.",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event():
    if not settings.MOCK_DATABASE:
        logger.info("Initializing vector database schemas...")
        neo4j_vector_store.initialize_vector_index()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Parametrize in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Multi-Tenant isolation validation
app.add_middleware(TenantValidatorMiddleware)

# Register routers
app.include_router(onboarding_router)
app.include_router(rag_router)


@app.get("/")
async def root():
    return {
        "status": "GCIP API Online",
        "version": "1.0.0",
        "environment": "development"
    }

@app.get("/health")
async def health_check():
    if settings.MOCK_DATABASE:
        return {
            "api": "healthy",
            "neo4j": "offline_mode",
            "redis": "offline_mode",
            "mock_database": True
        }
        
    neo4j_ok = neo4j_conn.verify_connectivity()
    redis_ok = redis_client.verify_connectivity()
    
    status_detail = {
        "api": "healthy",
        "neo4j": "connected" if neo4j_ok else "failed",
        "redis": "connected" if redis_ok else "failed",
        "mock_database": False
    }
    
    if not neo4j_ok or not redis_ok:
        raise HTTPException(status_code=503, detail=status_detail)
        
    return status_detail



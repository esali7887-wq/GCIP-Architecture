from app.config import settings
from app.database.interfaces import BaseProjectRepository
from app.database.mock_repository import mock_project_repo
from app.database.neo4j_connection import neo4j_conn
from app.database.neo4j_repository import Neo4jProjectRepository

def get_project_repository() -> BaseProjectRepository:
    """
    FastAPI dependency that returns the active project repository implementation.
    If MOCK_DATABASE is False and Neo4j connection is verified,
    it returns the real Neo4jProjectRepository.
    Otherwise, it falls back to the in-memory mock repository.
    """
    if not settings.MOCK_DATABASE:
        if neo4j_conn.verify_connectivity():
            return Neo4jProjectRepository()
    return mock_project_repo


import logging
from neo4j import GraphDatabase
from app.config import settings

logger = logging.getLogger("gcip-neo4j")

class Neo4jConnection:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            try:
                self.driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                    connection_timeout=2.0
                )
                logger.info("Neo4j driver initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Neo4j driver: {e}")
                raise e

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None
            logger.info("Neo4j driver closed.")

    def verify_connectivity(self) -> bool:
        try:
            self.connect()
            self.driver.verify_connectivity()
            logger.info("Neo4j connection verified successfully.")
            return True
        except Exception as e:
            logger.error(f"Neo4j connection verification failed: {e}")
            return False

neo4j_conn = Neo4jConnection()

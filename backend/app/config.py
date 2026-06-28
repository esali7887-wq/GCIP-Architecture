import os
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "gcipSecurePassword123")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    LOCAL_LLM_API: str = os.getenv("LOCAL_LLM_API", "http://127.0.0.1:11434")
    MOCK_DATABASE: bool = os.getenv("MOCK_DATABASE", "True").lower() in ("true", "1", "yes")

settings = Settings()


import logging
import redis
from app.config import settings

logger = logging.getLogger("gcip-redis")

class RedisClient:
    def __init__(self):
        self.client = None

    def connect(self):
        if not self.client:
            try:
                self.client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    decode_responses=True,
                    socket_connect_timeout=2.0,
                    socket_timeout=2.0
                )
                logger.info("Redis client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Redis client: {e}")
                raise e

    def verify_connectivity(self) -> bool:
        try:
            self.connect()
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis connection check failed: {e}")
            return False

redis_client = RedisClient()

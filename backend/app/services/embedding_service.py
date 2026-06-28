import os
import logging
import hashlib
import requests
from typing import List
from app.config import settings

logger = logging.getLogger("gcip-embedding-service")

class GeminiEmbeddingService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("No GEMINI_API_KEY or GOOGLE_API_KEY found in environment. Falling back to deterministic mock embeddings.")

    def get_embedding(self, text: str) -> List[float]:
        if not text:
            return [0.0] * 768

        if not self.api_key:
            return self._get_deterministic_mock_embedding(text)

        # Connect to Gemini Embedding API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={self.api_key}"
        payload = {
            "content": {
                "parts": [
                    {"text": text}
                ]
            }
        }
        try:
            response = requests.post(url, json=payload, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                return data["embedding"]["values"]
            else:
                logger.error(f"Gemini API returned error status {response.status_code}: {response.text}. Falling back to mock embeddings.")
                return self._get_deterministic_mock_embedding(text)
        except Exception as e:
            logger.error(f"Failed to connect to Gemini Embedding API: {e}. Falling back to mock embeddings.")
            return self._get_deterministic_mock_embedding(text)

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        # Batch processing falls back to single embeddings or direct API call if supported
        return [self.get_embedding(t) for t in texts]

    def _get_deterministic_mock_embedding(self, text: str) -> List[float]:
        # Generates a deterministic 768-dimensional float vector based on SHA-256 hash of the input text
        hash_obj = hashlib.sha256(text.encode("utf-8"))
        digest = hash_obj.digest()
        
        vector = []
        for i in range(768):
            # We derive floats from the digest using a deterministic modulo scheme
            val = digest[i % len(digest)]
            # Normalize to range [-1.0, 1.0]
            normalized = (val / 127.5) - 1.0
            # Scale slightly to make the vector dimensions mathematically distinct
            vector.append(normalized * (1.0 / (1.0 + (i % 10))))
        return vector

embedding_service = GeminiEmbeddingService()

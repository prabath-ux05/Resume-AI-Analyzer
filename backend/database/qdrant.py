import os
from qdrant_client import QdrantClient
from utils.logger import logger

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

qdrant_client = None

def init_qdrant():
    global qdrant_client
    try:
        qdrant_client = QdrantClient(url=QDRANT_URL)
        # Check connection
        collections = qdrant_client.get_collections()
        logger.info("Connected to Qdrant successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")

def get_qdrant():
    return qdrant_client

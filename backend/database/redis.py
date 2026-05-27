import os
import redis.asyncio as redis
from utils.logger import logger

REDIS_URL = os.getenv("REDIS_URL")

redis_client = None

async def init_redis():
    global redis_client

    if not REDIS_URL:
        redis_client = None
        logger.warning("REDIS_URL not set. Redis disabled.")
        return

    try:
        client = redis.from_url(REDIS_URL, decode_responses=True)
        await client.ping()
        redis_client = client
        logger.info("Connected to Redis successfully.")
    except Exception as e:
        redis_client = None
        logger.warning(f"Redis unavailable. Continuing without Redis: {e}")

async def close_redis():
    global redis_client

    if redis_client:
        await redis_client.close()
        redis_client = None

def get_redis():
    return redis_client
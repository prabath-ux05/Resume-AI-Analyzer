import json
from typing import List, Dict
from database.redis import get_redis

class RedisMemoryService:
    """
    Dedicated service for managing rolling conversation history in Redis.
    """
    
    @staticmethod
    async def get_history(session_id: str) -> List[Dict[str, str]]:
        """Fetch chat history from Redis."""
        redis = get_redis()
        if not redis:
            return []
        
        history_key = f"chat_history:{session_id}"
        cached = await redis.get(history_key)
        if cached:
            return json.loads(cached)
        return []

    @staticmethod
    async def save_history(session_id: str, history: List[Dict[str, str]]):
        """Save chat history to Redis with a 24-hour expiration."""
        redis = get_redis()
        if not redis:
            return
            
        history_key = f"chat_history:{session_id}"
        await redis.set(history_key, json.dumps(history), ex=86400)

    @staticmethod
    async def delete_history(session_id: str) -> bool:
        """Delete chat history from Redis."""
        redis = get_redis()
        if not redis:
            return False
            
        history_key = f"chat_history:{session_id}"
        result = await redis.delete(history_key)
        return result > 0

from fastapi import HTTPException, Request
from database.redis import get_redis
import logging

class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window

    async def __call__(self, request: Request):
        redis = get_redis()

        if not redis:
            return

        try:
            ip = request.client.host if request.client else "unknown"
            key = f"rate_limit:{ip}:{request.url.path}"

            current = await redis.get(key)

            if current and int(current) >= self.requests:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )

            pipe = redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, self.window)
            await pipe.execute()

        except HTTPException:
            raise

        except Exception as e:
            logging.warning(f"Redis rate limiter skipped: {e}")
            return
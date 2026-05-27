from fastapi import Request

class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window

    async def __call__(self, request: Request):
        # Redis disabled for Render Free deployment
        return
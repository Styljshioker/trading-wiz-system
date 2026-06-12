import redis.asyncio as redis
from .config import settings
import json
from typing import Any, Optional

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        if not self.redis:
            self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return self.redis
    
    async def ping(self):
        client = await self.connect()
        return await client.ping()
    
    async def set(self, key: str, value: Any, ex: Optional[int] = None):
        client = await self.connect()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await client.set(key, value, ex=ex)
    
    async def get(self, key: str) -> Optional[str]:
        client = await self.connect()
        return await client.get(key)
    
    async def get_json(self, key: str) -> Optional[dict]:
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    async def delete(self, key: str):
        client = await self.connect()
        return await client.delete(key)
    
    async def close(self):
        if self.redis:
            await self.redis.close()

# Global Redis client instance
redis_client = RedisClient()

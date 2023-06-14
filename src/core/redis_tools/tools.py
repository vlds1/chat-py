import json

import aioredis


class RedisCache:
    def __init__(self, redis_client: aioredis.Redis, ttl: int = 600) -> None:
        self.redis_client = redis_client

    async def redis_get_or_set(self, key: str, data: dict) -> dict:
        val = await self.redis_client.get(key)
        if val:
            print(
                "Live-time in cache remaining: ", await self.redis_client.ttl(key), "s"
            )
            return json.loads(val)
        await self.redis_client.set(key, value=json.dumps(data), ex=600)
        return data

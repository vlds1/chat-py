import json

import aioredis

from src.core.settings import settings

redis_client = aioredis.from_url(
    settings.redis_url, encoding="utf-8", decode_responses=True
)


async def redis_get_or_set(key: str, data: dict) -> dict:
    val = await redis_client.get(key)
    if val:
        print(
            "Live-time in cache remaining: ", await redis_client.ttl(key), "s"
        )
        return json.loads(val)
    await redis_client.set(key, value=json.dumps(data), ex=settings.redis_ttl)
    return data

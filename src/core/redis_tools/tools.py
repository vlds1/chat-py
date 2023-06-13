import json

import aioredis

from src.core.settings import settings


redis_cache = aioredis.from_url(
    settings.redis_cache_url, encoding="utf-8", decode_responses=True
)


async def redis_get_or_set(key: str, data: dict) -> dict:
    val = await redis_cache.get(key)
    if val:
        print(
            "Live-time in cache remaining: ", await redis_cache.ttl(key), "s"
        )
        return json.loads(val)
    await redis_cache.set(key, value=json.dumps(data), ex=settings.redis_ttl)
    return data

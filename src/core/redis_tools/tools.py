import json

import aioredis
from src.core.settings import settings

redis_client = aioredis.from_url(settings.redis_url, encoding='utf-8', decode_responses=True)


async def redis_get_or_set(key, data):
    val = await redis_client.hgetall(key)
    if val:
        return val
    await redis_client.hmset(key, mapping=data)
    return data


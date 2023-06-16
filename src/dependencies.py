from fastapi import Depends
import aioredis
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from src.api.weather.crud import MongoExtractor, MongoWriter
from src.core.settings.settings import Settings
from src.core.redis_tools.tools import RedisCache


async def get_settings() -> Settings:
    """Получение и кэширование настроек проекта."""
    return Settings()  # type: ignore


async def get_redis_client(settings: Settings = Depends(get_settings)):
    return aioredis.from_url(
        settings.redis_cache_url, encoding="utf-8", decode_responses=True
    )


async def get_redis_cache(
    redis_client: aioredis.Redis = Depends(get_redis_client),
    settings: Settings = Depends(get_settings),
) -> RedisCache:
    return RedisCache(redis_client=redis_client, ttl=settings.redis_ttl)


async def get_mongo_client(
    settings: Settings = Depends(get_settings),
) -> "AsyncIOMotorClient":
    return AsyncIOMotorClient(settings.mongodb_url)


async def get_mongo_connection(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
):
    return mongo_client.weather_app


async def get_mongo_collection(
    database: AsyncIOMotorDatabase = Depends(get_mongo_connection),
    collection_name: str = "weather_data",
) -> AsyncIOMotorCollection:
    return database.get_collection(collection_name)


async def get_mongo_exctructor(
    collection: AsyncIOMotorCollection = Depends(get_mongo_collection),
    redis_cache: RedisCache = Depends(get_redis_cache),
):
    return MongoExtractor(collection, redis_cache)


async def get_mongo_writer(
    collection: AsyncIOMotorCollection = Depends(get_mongo_collection),
):
    return MongoWriter(collection)

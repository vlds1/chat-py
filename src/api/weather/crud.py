from typing import Any, Mapping, Optional
from fastapi import Depends
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.main import ModelMetaclass

from src.api.types import WeatherSchema
from src.core.redis_tools.tools import RedisCache


class MongoExtractor:
    """
    Class that allows getting data from MongoDB
    """

    def __init__(
        self, collection: AsyncIOMotorCollection, redis_cache: RedisCache
    ) -> None:
        self.collection = collection
        self.redis_cache = redis_cache

    async def get_latest_one(self, city: str) -> Optional[Mapping[Any, Any]]:
        document = await self.collection.find_one(
            {"city": city}, {"_id": 0}, sort=[("_id", -1)], limit=1
        )
        return await self.redis_cache.redis_get_or_set(key=city, data=document)

    async def get_many(self, schema: ModelMetaclass) -> list:
        return [schema(**doc) async for doc in self.collection.find()]


class MongoWriter:
    """
    Class which makes records in mongoDB
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def create_record(
        self, input_data: WeatherSchema = Depends()
    ) -> int:
        await self.collection.insert_one(input_data.dict())
        return status.HTTP_200_OK

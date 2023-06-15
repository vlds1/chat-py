from fastapi import Depends
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic.main import ModelMetaclass

from src.api.weather.schemas import WeatherSchema
from src.core.redis_tools.tools import redis_get_or_set


class MongoExtractor:
    """
    Class that allows getting data from MongoDB
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def get_latest_one(self, city: str) -> dict:
        document = await self.collection.find_one(
            {"city": city}, {"_id": 0}, sort=[("_id", -1)], limit=1
        )
        return await redis_get_or_set(key=city, data=document)

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
        await self.collection.insert_one(input_data)
        return status.HTTP_200_OK

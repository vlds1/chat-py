from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.testing.config import db_url

from src.core.settings.mongodb import weather_data_collection, weather_helper


async def create_record(input_data: dict) -> dict:
    mongo_client = AsyncIOMotorClient(db_url)
    db = mongo_client["weather_app"]
    collection = db["weather_data"]

    await collection.insert_one(input_data)
    return status.HTTP_200_OK


async def get_records() -> list:
    documents = []
    async for doc in weather_data_collection.find():
        documents.append(weather_helper(doc))
    return documents


async def get_latest_record(city: str) -> dict:
    document = await weather_data_collection.find_one({"city": city}, sort=[("_id", -1)], limit=1)
    return document

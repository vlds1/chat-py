import os
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.testing.config import db_url


async def create_record(input_data: dict) -> dict:
    mongo_client = AsyncIOMotorClient(db_url)
    db = mongo_client["weather_app"]
    collection = db["weather_data"]

    await collection.insert_one(input_data)
    return status.HTTP_200_OK

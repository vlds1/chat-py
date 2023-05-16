import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

db_ulr = os.environ.get("MONGODB_URL")


def get_mongo_client() -> "AsyncIOMotorClient":
    mongo_client = AsyncIOMotorClient(db_ulr)
    return mongo_client


db_client = get_mongo_client()
database = db_client.weather_app

# collections

weather_data_collection = database.get_collection("weather_data")

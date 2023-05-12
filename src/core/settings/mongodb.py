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


# helpers


def weather_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "city": str(data["city"]),
        "current_temperature": data["current_temperature"],
        "current_weather": data["current_weather"],
        "current_wind_speed": data["current_wind_speed"],
        "current_humidity": data["current_humidity"],
        "sunrise": data["sunrise"],
        "sunset": data["sunset"],
        "day_duration": data["day_duration"],
        "request_time": data["request_time"],
    }

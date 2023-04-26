import os

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

db_ulr = os.environ.get("MONGODB_URL")

mongo_client = AsyncIOMotorClient(db_ulr)
database = mongo_client.weather_app

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
    }

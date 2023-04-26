from fastapi import APIRouter
from src.core.settings.mongodb import weather_helper, weather_data_collection

routers = APIRouter()


@routers.get(
    "/get_records"
)
async def get_records() -> list:
    documents = []
    async for doc in weather_data_collection.find():
        documents.append(weather_helper(doc))
    return documents


from fastapi import APIRouter

from src.api.weather.crud import get_records

routers = APIRouter()


@routers.get(
    "/get_records"
)
async def get_all_records() -> list:
    result = await get_records()
    return result


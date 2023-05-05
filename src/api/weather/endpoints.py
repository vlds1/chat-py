import pickle
import time
from time import sleep

from fastapi import APIRouter, Path, Depends
from fastapi_cache.decorator import cache

from src.api.weather.utils import make_graphql_request
from src.api.weather.crud import get_records, get_latest_record
from src.core.redis_tools.tools import redis_get_or_set

routers = APIRouter()


@routers.get('/')
async def home() -> str:
    return "hello from API"


@routers.get(
    "/get_records"
)
@cache(expire=30)
async def get_all_records() -> list:
    sleep(5)
    result = await get_records()
    return result


@routers.get(
    "/get_record/{city}",
    response_model=None
)
@cache(expire=30)
async def get_latest_record_city(
        city: str = Path(),
) -> list:
    # sleep(5)
    result = await get_latest_record(city)
    return result


@routers.get("/weather/{city}", response_model=None)
async def get_graphql(
        city: str = Path()
) -> dict:

    weather_query = """
    query Weather {
    weather (city: "Rostov-on-Don"){
    	city
		current_temperature
        current_humidity
        current_weather
        current_wind_speed
        sunrise
        sunset
        day_duration
   }
}
    """
    response = await make_graphql_request(weather_query)
    data = await redis_get_or_set(key="2", data=response)
    return data

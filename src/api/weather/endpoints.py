from fastapi import APIRouter
from fastapi import Path

from src.api.query_schemas.queries import weather_query
from src.api.weather.schemas import WeatherSchema
from src.api.weather.utils import get_weather_data

routers = APIRouter()


@routers.get(
    "/weather/{city}",
    response_model=WeatherSchema,
)
async def get_weather(city: str = Path()) -> WeatherSchema:
    variables = {"city": city}
    response = await get_weather_data(weather_query, variables)
    return WeatherSchema(**response["data"]["CityWeather"])

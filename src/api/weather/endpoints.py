from fastapi import APIRouter, HTTPException
from fastapi import Path

from src.api.query_schemas.queries import weather_query
from src.api.types import WeatherSchema
from src.api.weather.utils import get_weather_data

routers = APIRouter()


@routers.get(
    "/weather/{city}",
    response_model=WeatherSchema,
    name="get_weather",
)
async def get_weather(city: str = Path()) -> WeatherSchema:
    variables = {"city": city}
    response = await get_weather_data(weather_query, variables)
    if response["data"]["CityWeather"] is None:
        raise HTTPException(status_code=404, detail="City not found")
    return WeatherSchema(**response["data"]["CityWeather"])

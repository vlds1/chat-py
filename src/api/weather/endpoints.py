from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi_limiter.depends import RateLimiter

from src.api.query_schemas.queries import weather_query
from src.api.weather.schemas import WeatherSchema
from src.api.weather.utils import make_graphql_request

routers = APIRouter()


@routers.get(
    "/weather/{city}",
    response_model=WeatherSchema,
    dependencies=[
        Depends(RateLimiter(times=5, seconds=10)),
    ],
)
async def get_graphql(city: str = Path()) -> WeatherSchema:
    variables = {"city": city}
    response = await make_graphql_request(weather_query, variables)
    return WeatherSchema(**response["data"]["CityWeather"])

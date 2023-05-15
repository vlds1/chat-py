from fastapi import APIRouter
from fastapi import Path

from src.api.query_schemas.queries import weather_query
from src.api.weather.schemas import WeatherSchema
from src.api.weather.utils import make_graphql_request

routers = APIRouter()


@routers.get("/weather/{city}", response_model=None)
async def get_graphql(city: str = Path()) -> WeatherSchema:
    variables = {"city": city}
    response = await make_graphql_request(weather_query, variables)
    print(response)
    return response

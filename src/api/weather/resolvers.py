from ariadne import load_schema_from_path
from ariadne import make_executable_schema
from ariadne import ObjectType
from ariadne.asgi import GraphQL

from src.api.weather.crud import get_latest_record

query = ObjectType("WeatherQuerySchema")
type_defs = load_schema_from_path("src/api/query_schemas/schema.graphql")


@query.field("CityWeather")
async def resolve_get_city_weather(_, info, city="Moscow"):
    data = await get_latest_record(city)
    return data


schema = make_executable_schema(
    type_defs,
    [
        query,
    ],
)
graphql_app = GraphQL(schema, debug=True)

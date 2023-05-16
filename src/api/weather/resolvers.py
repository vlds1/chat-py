from ariadne import load_schema_from_path
from ariadne import make_executable_schema
from ariadne import ObjectType
from ariadne.asgi import GraphQL

from src.api.weather.crud import MongoExtractor
from src.core.settings.mongodb import weather_data_collection

query = ObjectType("WeatherQuerySchema")
type_defs = load_schema_from_path("src/api/query_schemas/schema.graphql")


@query.field("CityWeather")
async def resolve_get_city_weather(_, info, city="Moscow"):
    db = MongoExtractor(collection=weather_data_collection)
    return await db.get_latest_one(city=city)


schema = make_executable_schema(
    type_defs,
    [
        query,
    ],
)
graphql_app = GraphQL(schema, debug=True)

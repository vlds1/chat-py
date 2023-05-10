from enum import Enum

from ariadne import gql, make_executable_schema, ObjectType, load_schema_from_path
from ariadne.asgi import GraphQL

from src.api.weather.crud import get_latest_record

query = ObjectType("Query")
type_defs = load_schema_from_path("src/api/weather/schema.graphql")


class Cities(Enum):

    MOSCOW = 'Moscow'
    ROSTOV_ON_DON = 'Rostov-on-Don'
    BERLIN = 'Berlin'
    WASHINGTON = 'Washington'
    KIEV = 'Kyiv'
    MINSK = 'Minsk'
    PARIS = 'Paris'


@query.field("GetCityWeather")
async def resolve_get_city_weather(_, info, city="Moscow"):
    data = await get_latest_record(city)
    print('data:', data)
    return data


schema = make_executable_schema(type_defs, [query, ])
graphql_app = GraphQL(schema, debug=True)




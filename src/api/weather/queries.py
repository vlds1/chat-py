from enum import Enum

from ariadne import gql, make_executable_schema, ObjectType
from ariadne.asgi import GraphQL
from src.core.redis_tools.tools import redis_get_or_set
from src.api.weather.endpoints import get_latest_record_city

query = ObjectType("Query")


class Cities(Enum):

    MOSCOW = 'Moscow'
    ROSTOV_ON_DON = 'Rostov-on-Don'
    BERLIN = 'Berlin'
    WASHINGTON = 'Washington'
    KIEV = 'Kyiv'
    MINSK = 'Minsk'
    PARIS = 'Paris'


type_defs = gql("""
    type Query {
        weather(city: String): GetCityWeather
    }
    
    type GetCityWeather {
        _id: String
        city: String!
        current_temperature: Float!
        current_humidity: Int!
        current_weather: String!
        current_wind_speed: Float!
        sunrise: String!
        sunset: String!
        day_duration: String!
    }
""")


@query.field("weather")
async def resolve_get_city_weather(_, info, city="Moscow"):
    data = await get_latest_record_city(city)
    result = await redis_get_or_set(key=city, data=data)
    print('data:', data)
    return result


schema = make_executable_schema(type_defs, [query, ])
graphql_app = GraphQL(schema, debug=True)




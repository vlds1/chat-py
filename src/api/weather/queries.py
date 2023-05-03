from ariadne import gql, make_executable_schema, ObjectType
from ariadne.asgi import GraphQL

from src.api.weather.crud import get_latest_record

query = ObjectType("Query")

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
    data = await get_latest_record(city)
    return data


schema = make_executable_schema(type_defs, [query, ])
graphql_app = GraphQL(schema, debug=True)

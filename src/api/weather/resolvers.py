from src.api.weather.context_types import GraphQLResolveInfo, query

@query.field("CityWeather")
async def resolve_get_city_weather(_, info: GraphQLResolveInfo, city="Moscow"):
    return await info.context.mongo_extractor.get_latest_one(city=city)
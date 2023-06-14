import aiohttp
from fastapi import Depends
from src.dependencies import get_settings


async def get_weather_data(query: str, variables: dict[str, str]) -> dict:
    async with aiohttp.ClientSession() as session:
        settings = await get_settings()
        payload = {"query": query, "variables": variables}
        async with session.post(
            url=settings.graphql_url, json=payload
        ) as response:
            return await response.json()


async def string_decoder(data_string: str) -> dict:
    data_dict = dict()
    pairs = data_string.split()
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=")
            value = value.strip('"')
            data_dict[key] = value
    return data_dict

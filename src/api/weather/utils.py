import asyncio

import aiohttp
from aiokafka import AIOKafkaConsumer

from src.core.settings import settings


async def get_consumer() -> AIOKafkaConsumer:
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        loop=loop,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_consumer_group,
    )
    return consumer


async def get_weather_data(query: str, variables: dict[str, str]) -> dict:
    async with aiohttp.ClientSession() as session:
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

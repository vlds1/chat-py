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


async def make_graphql_request(query: str, variables: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        payload = dict({"query": query, "variables": variables})
        print(payload)
        async with session.post(
            url=settings.graphql_url, json=payload
        ) as response:
            return await response.json()

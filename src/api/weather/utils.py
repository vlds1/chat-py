import asyncio
from aiokafka import AIOKafkaConsumer
from src.core.settings import settings


async def get_consumer() -> AIOKafkaConsumer:
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(settings.kafka_topic,
                                loop=loop,
                                bootstrap_servers=settings.kafka_bootstrap_servers,
                                group_id=settings.kafka_consumer_group)
    return consumer

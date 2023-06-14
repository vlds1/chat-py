import asyncio
from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter
from src.core.settings.settings import Settings

from src.api.weather.crud import MongoWriter
from src.api.weather.utils import string_decoder

routers = APIRouter()


class Consumer:
    """
    Allows to consume data from Kafka container
    """

    def __init__(self, collection, settings: Settings):
        self.db = MongoWriter(collection=collection)
        self.consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            settings.kafka_topic,
            loop=asyncio.get_event_loop(),
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_consumer_group,
        )


    async def start_consumer(self):
        await self.consumer.start()

    async def stop_consumer(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume(self):
        await self.start_consumer()
        try:
            async for msg in self.consumer:
                data = msg.value.decode("utf-8")
                result = await string_decoder(data.replace("'", '"'))
                print("Consumed data:", result)
                await self.db.create_record(result)
        finally:
            await self.stop_consumer()

from fastapi import APIRouter

from src.api.weather.crud import MongoWriter
from src.api.weather.utils import get_consumer
from src.api.weather.utils import string_decoder

routers = APIRouter()


class Consumer:
    """
    Allows to consume data from Kafka container
    """

    def __init__(self, collection):
        self.db = MongoWriter(collection=collection)
        self.consumer = None

    async def start_consumer(self):
        self.consumer = await get_consumer()
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

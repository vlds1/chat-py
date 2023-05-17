import asyncio

from fastapi import APIRouter

from src.api.weather.crud import MongoWriter
from src.api.weather.utils import get_consumer
from src.api.weather.utils import string_decoder
from src.core.settings.mongodb import weather_data_collection

routers = APIRouter()


class Consumer:
    """
    Allows to consume data from kafka container
    """

    @staticmethod
    async def consume():
        db = MongoWriter(collection=weather_data_collection)
        consumer = await get_consumer()
        await consumer.start()
        try:
            async for msg in consumer:
                data = msg.value.decode("utf-8")
                result = await string_decoder(data.replace("'", '"'))
                print("Consumed data: ", result)
                await db.create_record(result)
        finally:
            await consumer.stop()


asyncio.create_task(Consumer.consume())

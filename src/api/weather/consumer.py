import asyncio
import json

from fastapi import APIRouter

from src.api.weather.crud import MongoWriter
from src.api.weather.utils import get_consumer

routers = APIRouter()


class Consumer:
    """
    Allows to consume data from kafka container
    """

    @staticmethod
    async def consume():
        consumer = await get_consumer()
        await consumer.start()
        try:
            async for msg in consumer:
                data = msg.value.decode("utf-8")
                result = json.loads(data.replace("'", '"'))
                print("Consumed data: ", result)
                await MongoWriter.create_record(result)
        finally:
            await consumer.stop()


asyncio.create_task(Consumer.consume())

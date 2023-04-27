import asyncio
import json
from fastapi import APIRouter
from src.api.weather.utils import get_consumer
from src.api.weather.crud import create_record

routers = APIRouter()


async def consume():
    consumer = await get_consumer()
    await consumer.start()
    try:
        async for msg in consumer:
            data = msg.value.decode("utf-8")
            result = json.loads(data.replace("'", '"'))
            print(result)
            await create_record(result)
    finally:
        await consumer.stop()

asyncio.create_task(consume())

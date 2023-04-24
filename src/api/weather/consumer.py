import asyncio
import json
import os
from dotenv import load_dotenv

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter

routers = APIRouter()
loop = asyncio.get_event_loop()
load_dotenv()
topic = os.environ.get("KAFKA_TOPIC")
servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
group = os.environ.get("KAFKA_CONSUMER_GROUP")


async def consume():
    consumer = AIOKafkaConsumer(topic,
                                loop=loop,
                                bootstrap_servers=servers,
                                group_id=group)
    await consumer.start()
    try:
        async for msg in consumer:
            data = msg.value.decode("utf-8")
            result = json.loads(data.replace("'", '"'))
            # здесь будет запись в mongoDB

    finally:
        await consumer.stop()

asyncio.create_task(consume())

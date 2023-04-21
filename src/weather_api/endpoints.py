import json
import os
from fastapi import APIRouter, Path

from weather_api.main import get_weather
from weather_api.schema import WeatherSchema
from dotenv import load_dotenv
import asyncio
from aiokafka import AIOKafkaProducer

load_dotenv()

routers = APIRouter()

loop = asyncio.get_event_loop()

topic = os.environ.get("KAFKA_TOPIC")
servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
group = os.environ.get("KAFKA_CONSUMER_GROUP")


@routers.get('/')
async def home():
    return "hello from API"


@routers.get(
    '/get_weather/{city}',
    name="weather_api:get_weather",
    response_model=WeatherSchema
)
async def send_weather(
        city: str = Path()
):
    producer = AIOKafkaProducer(loop=loop,
                                bootstrap_servers=servers,
                                )
    await producer.start()
    try:
        print(f'Sending weather_api in city: {city}')
        data = await get_weather(city)

        await producer.send_and_wait(topic, bytes(str(data), "utf-8"))

    finally:
        await producer.stop()

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path

from src.core.settings import settings
from src.weather_api.schema import WeatherSchema
from src.weather_api.services import get_weather
from src.weather_api.utils import get_producer

routers = APIRouter()


@routers.get("/")
async def home() -> str:
    return "hello from API"


@routers.get(
    "/get_weather/{city}",
    name="weather_api:get_weather",
    response_model=WeatherSchema,
)
async def send_weather(
    city: str = Path(), producer: AIOKafkaProducer = Depends(get_producer)
) -> dict:
    await producer.start()
    try:
        print(f"Sending weather_api in city: {city}")
        data = await get_weather(city)
        await producer.send_and_wait(
            settings.kafka_topic, bytes(str(data), "utf-8")
        )
        return WeatherSchema(**data)
    finally:
        await producer.stop()

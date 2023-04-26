import asyncio
import datetime
from src.core.settings import settings
from aiokafka import AIOKafkaProducer


async def extract_weather_data(data: dict) -> dict:
    city = data["name"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind = data["wind"]["speed"]
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    day_duration = sunset - sunrise
    return {
        "city": city,
        "current_temperature": temperature,
        "current_humidity": humidity,
        "current_weather": weather,
        "current_wind_speed": wind,
        "sunrise": sunrise.strftime("%m.%d.%Y %H:%M:%S"),
        "sunset": sunset.strftime("%m.%d.%Y %H:%M:%S"),
        "day_duration": str(day_duration)
    }


async def get_producer():
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.kafka_bootstrap_servers)
    return producer

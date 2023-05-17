import asyncio
import datetime

import requests
from aiokafka import AIOKafkaProducer
from pydantic.main import ModelMetaclass

from src.core.settings import settings
from src.weather_api.schema import WeatherSchema


async def extract_weather_data(
    data: dict, schema: ModelMetaclass
) -> WeatherSchema:
    city = data["name"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind = data["wind"]["speed"]
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    day_duration = sunset - sunrise
    return schema(
        city=city,
        current_temperature=temperature,
        current_humidity=humidity,
        current_weather=weather,
        current_wind_speed=wind,
        sunrise=sunrise.strftime("%H:%M:%S"),
        sunset=sunset.strftime("%H:%M:%S"),
        day_duration=str(day_duration),
        request_time=datetime.datetime.now().strftime("%H:%M:%S - %Y-%m-%d"),
    )


async def get_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=settings.kafka_bootstrap_servers
    )
    return producer


async def get_weather(city: str) -> dict:
    try:
        r = requests.get(
            url=settings.openweather_url,
            params={
                "q": city,
                "appid": settings.open_weather_token,
                "units": "metric",
            },
        )
        data = r.json()
        result = await extract_weather_data(data, schema=WeatherSchema)
        return result
    except ValueError:
        raise ValueError("Check city name")

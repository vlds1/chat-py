import asyncio
import os


import requests
from dotenv import load_dotenv
from src.weather_api.utils import extract_weather_data

load_dotenv()

token = os.environ.get("OPEN_WEATHER_TOKEN")


async def get_weather(city: str, weather_token: str = token) -> dict:
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
        )
        data = r.json()
        result = await extract_weather_data(data)
        return result
    except Exception as ex:
        raise Exception("Check city name")


async def main():
    city = input("city: ")
    await get_weather(city, weather_token=token)


if __name__ == "__main__":
    asyncio.run(main())

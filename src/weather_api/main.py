import asyncio
import os


import requests
from dotenv import load_dotenv
import datetime

load_dotenv()

token = os.environ.get("OPEN_WEATHER_TOKEN")


async def get_weather(city, weather_token=token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_temp = data["main"]["temp"]
        cur_humidity = data["main"]["humidity"]
        cur_weather = data["weather"][0]["description"]
        cur_wind = data["wind"]["speed"]
        sunrise_timestampt = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestampt = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day_duration = sunset_timestampt - sunrise_timestampt

        return {
            "city": city,
            "current_temperature": cur_temp,
            "current_weather": cur_weather,
            "current_wind_speed": cur_wind,
            "current_humidity": cur_humidity,
            "sunrise": sunrise_timestampt.strftime("%m.%d.%Y %H:%M:%S"),
            "sunset": sunset_timestampt.strftime("%m.%d.%Y %H:%M:%S"),
            "day_duration": str(day_duration)
        }

    except Exception as ex:
        raise Exception("Check city name")


async def main():
    city = input("city: ")
    await get_weather(city, weather_token=token)


if __name__ == "__main__":
    asyncio.run(main())

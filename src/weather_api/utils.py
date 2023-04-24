import datetime


async def extract_weather_data(data):
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

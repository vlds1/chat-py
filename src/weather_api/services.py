from src.core.settings import settings
import requests
from src.weather_api.utils import extract_weather_data


async def get_weather(city: str,
                      weather_token: str = settings.open_weather_token) -> dict:
    try:
        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": weather_token, "units": "metric"}
        )
        data = r.json()
        result = await extract_weather_data(data)
        return result
    except ...:
        raise ValueError("Check city name")

from async_asgi_testclient import TestClient
from src.api.weather.utils import get_weather_data


async def test_get_weather_data(test_client: TestClient):
    async def mock_get_weather_data(query: str, variables: dict[str, str]) -> dict:
        return {"data": {"CityWeather": {'city': 'Moscow', 
                    'current_temperature': 25, 
                    'current_humidity': 50, 
                    'current_weather': 'Clear', 
                    'current_wind_speed': 1.32, 
                    'sunrise': '03:47:09', 
                    'sunset': '21:10:28', 
                    'day_duration': '17:23:19', 
                    'request_time': '15:56:07'}}}


    original_get_weather_data = get_weather_data
    get_weather_data.__code__ = mock_get_weather_data.__code__

    city = "Moscow"
    response = await test_client.get(f"/api/weather/{city}")
    assert response.status_code == 200


    get_weather_data.__code__ = original_get_weather_data.__code__

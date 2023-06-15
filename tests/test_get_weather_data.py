from unittest.mock import AsyncMock, patch
from fastapi import status
import pytest
from async_asgi_testclient import TestClient
from src.main import settings
from src.api.weather.utils import get_weather_data
from aioresponses import aioresponses
    

@pytest.mark.asyncio
async def test_check_invalid_city(test_client: TestClient):
    mock_return_value = {"data": {"CityWeather": {'city': 'Moscow', 
                'current_temperature': 25, 
                'current_humidity': 50, 
                'current_weather': 'Clear', 
                'current_wind_speed': 1.32, 
                'sunrise': '03:47:09', 
                'sunset': '21:10:28', 
                'day_duration': '17:23:19', 
                'request_time': '15:56:07'}}}
    
    city = "UnknownCity"
    with aioresponses() as mocked:
        mocked.post(settings.graphql_url, payload=mock_return_value)
        
        response = await test_client.get(f"/api/weather/{city}")
        assert response.json() != {'city': 'UnknownCity', 
                    'current_temperature': 0, 
                    'current_humidity': 0, 
                    'current_weather': 'Clear', 
                    'current_wind_speed': 0, 
                    'sunrise': '00:00:00', 
                    'sunset': '10:10:10', 
                    'day_duration': '66:66:66', 
                    'request_time': '15:15:15'}



@pytest.mark.asyncio
async def test_get_weather_data(test_client):

    with aioresponses() as mocked:
        mocked.post(settings.graphql_url, payload={"data": {
            "CityWeather": {
                'city': 'Moscow', 
                'current_temperature': 25, 
                'current_humidity': 50, 
                'current_weather': 'Clear', 
                'current_wind_speed': 1.32, 
                'sunrise': '03:47:09', 
                'sunset': '21:10:28', 
                'day_duration': '17:23:19', 
                'request_time': '15:56:07'
            }
        }})

        city = "Moscow"
        response = await test_client.get(f"/api/weather/{city}")
        print(response.json())
        assert response.json() == {
                'city': 'Moscow', 
                'current_temperature': 25, 
                'current_humidity': 50, 
                'current_weather': 'Clear', 
                'current_wind_speed': 1.32, 
                'sunrise': '03:47:09', 
                'sunset': '21:10:28', 
                'day_duration': '17:23:19', 
                'request_time': '15:56:07'
            }



@pytest.mark.parametrize(
    "city, mock_return_value, expected_response, expected_status_code",
    [
        (
            "Rostov-on-Don", 
            {"data": {"CityWeather": {'city': "Rostov-on-Don", 
                'current_temperature': 22.05, 
                'current_humidity': 56, 
                'current_weather': 'overcast', 
                'current_wind_speed': 2.96, 
                'sunrise': "04:24:39", 
                'sunset': "20:18:07", 
                'day_duration': "15:53:28", 
                'request_time': "13:35:49"}}},
            {'city': "Rostov-on-Don", 
                'current_temperature': 22.05, 
                'current_humidity': 56, 
                'current_weather': 'overcast', 
                'current_wind_speed': 2.96, 
                'sunrise': "04:24:39", 
                'sunset': "20:18:07", 
                'day_duration': "15:53:28", 
                'request_time': "13:35:49"}, status.HTTP_200_OK
        ),
        (
            "New York",
            {"data": {"CityWeather": {'city': "New York", 
                'current_temperature': 27.05, 
                'current_humidity': 60, 
                'current_weather': 'Sunny', 
                'current_wind_speed': 3.50, 
                'sunrise': "05:24:39", 
                'sunset': "19:18:07",
                'day_duration': "13:53:28", 
                'request_time': "14:35:49"}}},
            {'city': "New York", 
                'current_temperature': 27.05, 
                'current_humidity': 60, 
                'current_weather': 'Sunny', 
                'current_wind_speed': 3.50, 
                'sunrise': "05:24:39", 
                'sunset': "19:18:07",
                'day_duration': "13:53:28", 
                'request_time': "14:35:49"}, status.HTTP_200_OK
        ),
        (
            "Tokyo",
            {"data": {"CityWeather": {'city': "Tokyo", 
                'current_temperature': 30.05, 
                'current_humidity': 65, 
                'current_weather': 'Cloudy', 
                'current_wind_speed': 2.50, 
                'sunrise': "04:50:39", 
                'sunset': "18:30:07",
                'day_duration': "13:39:28", 
                'request_time': "15:35:49"}}},
            {'city': "Tokyo", 
                'current_temperature': 30.05, 
                'current_humidity': 65, 
                'current_weather': 'Cloudy', 
                'current_wind_speed': 2.50, 
                'sunrise': "04:50:39", 
                'sunset': "18:30:07",
                'day_duration': "13:39:28", 
                'request_time': "15:35:49"}, status.HTTP_200_OK
        ),
        (
            "Sydney",
            {"data": {"CityWeather": {'city': "Sydney", 
                'current_temperature': 25.05, 
                'current_humidity': 70, 
                'current_weather': 'Rain', 
                'current_wind_speed': 3.20, 
                'sunrise': "06:24:39", 
                'sunset': "20:18:07",
                'day_duration': "13:53:28", 
                'request_time': "16:35:49"}}},
            {'city': "Sydney", 
                'current_temperature': 25.05, 
                'current_humidity': 70, 
                'current_weather': 'Rain', 
                'current_wind_speed': 3.20, 
                'sunrise': "06:24:39", 
                'sunset': "20:18:07",
                'day_duration': "13:53:28", 
                'request_time': "16:35:49"}, status.HTTP_200_OK
        ),
        (
            "UknownCity",
            {'data': {'CityWeather': None}},
            {'detail': 'City not found'}, status.HTTP_404_NOT_FOUND
        ),

    ],
)
async def test_check_weather_in_cities(test_client: TestClient, 
                                       city, 
                                       mock_return_value, 
                                       expected_response, 
                                       expected_status_code):
    with aioresponses() as mocked:
        mocked.post(settings.graphql_url, payload=mock_return_value)
        

        response = await test_client.get(f"/api/weather/{city}")
        print(response.json())
        assert response.json() == expected_response
        assert response.status_code == expected_status_code
        
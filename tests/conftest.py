import pytest
import mongomock
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.settings.settings import Settings
from src.main import get_application

# policy = asyncio.WindowsSelectorEventLoopPolicy()
# asyncio.set_event_loop_policy(policy)


@pytest.fixture
async def settings():
    return Settings(
        mongodb_url="mongodb://localhost:27018",
    )


@pytest.fixture
def test_app(settings: Settings):
    return get_application(settings=settings)


@pytest.fixture
async def test_client(test_app: FastAPI):
    async with TestClient(test_app) as client:
        yield client


@pytest.fixture
def db(settings: Settings):
    client = AsyncIOMotorClient(settings.mongodb_url)
    yield client["test_db"]


def get_test_mongo_client():
    return AsyncIOMotorClient("mongodb://localhost:27018")


@pytest.fixture(scope="function")
def mock_db():
    mock_client = mongomock.MongoClient()
    db = mock_client.db
    yield db
    mock_client.close()


@pytest.fixture
def moscow_weather_preset():
    return {
        "data": {
            "CityWeather": {
                "city": "Moscow",
                "current_temperature": 24.24,
                "current_humidity": 28,
                "current_weather": "clear",
                "current_wind_speed": 3.33,
                "sunrise": "03:44:40",
                "sunset": "21:15:16",
                "day_duration": "17:30:36",
                "request_time": "12:34:25",
            }
        }
    }

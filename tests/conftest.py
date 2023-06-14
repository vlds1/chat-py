import pytest

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


# async def start_application():
#     redis = await get_redis_client()
#     FastAPICache.init(RedisBackend(), prefix="fastapi-cache")
#     app.state.db_client = db_client

#     asyncio.get_event_loop().run_until_complete(consumer.consume())
#     asyncio.get_event_loop().run_until_complete(
#         FastAPILimiter.init(redis_cache)
#     )


# def stop_application():
#     asyncio.create_task(consumer.stop_consumer())


# @pytest.fixture(autouse=True)
# def setup_and_teardown():
#     start_application()
#     yield
#     stop_application()

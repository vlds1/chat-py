import asyncio

import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.redis_tools.tools import redis_cache
from src.core.settings.mongodb import db_client
from src.core.settings.mongodb import get_mongo_client
from src.main import app
from src.main import consumer

policy = asyncio.WindowsSelectorEventLoopPolicy()
asyncio.set_event_loop_policy(policy)


@pytest.fixture
def client():
    app.dependency_overrides[get_mongo_client] = get_test_mongo_client
    client = TestClient(app)
    yield client


@pytest.fixture
def db():
    client = AsyncIOMotorClient("mongodb://localhost:27018")
    yield client["test_db"]


def get_test_mongo_client():
    return AsyncIOMotorClient("mongodb://localhost:27018")


def start_application():
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    app.state.db_client = db_client

    asyncio.get_event_loop().run_until_complete(consumer.consume())
    asyncio.get_event_loop().run_until_complete(
        FastAPILimiter.init(redis_cache)
    )


def stop_application():
    asyncio.create_task(consumer.stop_consumer())


@pytest.fixture(autouse=True)
def setup_and_teardown():
    start_application()
    yield
    stop_application()

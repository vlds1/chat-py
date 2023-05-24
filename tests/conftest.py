import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pymongo import MongoClient

from src.api import routers
from src.main import settings

policy = asyncio.WindowsSelectorEventLoopPolicy()
asyncio.set_event_loop_policy(policy)


@pytest.fixture
def test_app():
    test_app = FastAPI()
    test_app.include_router(routers, prefix=settings.api_prefix)
    return test_app


# @pytest.fixture
# def client():
#     with TestClient(test_app) as client:
#         yield client


# @pytest.fixture
# async def async_client(test_app):
#     async with TestClient(application=test_app) as ac:
#         yield ac


@pytest.fixture
async def async_client(test_app):
    async with AsyncClient(app=test_app, trust_env=True, verify=False) as ac:
        yield ac


# @pytest_asyncio.fixture
# async def async_client():
#     test_app: FastAPI = get_application()
#     async with AsyncClient(app=test_app) as ac:
#         yield ac


@pytest.fixture
def mongo_client():
    client = MongoClient("mongodb://localhost:27018/")
    client.server_info()
    test_db = client["test_database"]
    yield client, test_db
    client.drop_database("test_database")
    client.close()

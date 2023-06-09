# import asyncio
#
# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from fastapi_limiter import FastAPILimiter
# from motor.motor_asyncio import AsyncIOMotorClient
#
# from src.core.redis_tools.tools import get_redis_client
# from src.core.settings.mongodb import get_mongo_client
# from src.api import routers
# from src.main import settings, app
#
#
# policy = asyncio.WindowsSelectorEventLoopPolicy()
# asyncio.set_event_loop_policy(policy)
# redis = get_redis_client()
#
#
# def get_test_mongo_client():
#     return AsyncIOMotorClient('mongodb://localhost:27017')
#
# def override_get_mongo_client():
#     return get_test_mongo_client
#
# app.dependency_overrides[get_mongo_client] = override_get_mongo_client
#
# # Initialize FastAPILimiter
# asyncio.run(FastAPILimiter.init(redis))
#
# @pytest.fixture(scope="session")
# def test_client():
#     with TestClient(app) as test_client:
#         yield test_client

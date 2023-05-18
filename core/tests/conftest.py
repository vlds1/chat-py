import pytest
from pymongo.mongo_client import MongoClient

from core.app import app


@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield test_app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture()
def get_test_users_collection():
    client = MongoClient("mongodb://localhost:27017/chat-test")
    database = client.chat
    users_collection = database.get_collection("users")
    return users_collection


@pytest.fixture()
def user_data():
    user = {"email": "vlad.sergienko01@yandex.ru", "password": "passw124ord"}
    return user

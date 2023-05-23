import pytest
from pymongo.mongo_client import MongoClient

from core import create_app


@pytest.fixture()
def app():
    app = create_app(
        mongo_url="mongodb://localhost:27017/chat-test", db_name="chat-test"
    )
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app

    client = MongoClient("mongodb://localhost:27017/chat-test")
    db = client["chat-test"]
    db.drop_collection("users")


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def user_data():
    user = {"email": "xxx@yandex.ru", "password": "passw124ord"}
    return user


@pytest.fixture()
def registered_user(user_data, client):
    res = client.post("/api/v1/auth/registration", json=user_data)
    return res

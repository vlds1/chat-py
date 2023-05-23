import motor.motor_asyncio

from core.config import get_config


def get_users_collection():
    config = get_config()
    client = motor.motor_asyncio.AsyncIOMotorClient(config.DB_URL)
    database = client[config.DB_NAME]
    users_collection = database.get_collection("users")

    return users_collection

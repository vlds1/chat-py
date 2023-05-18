import motor.motor_asyncio

from core.config import config


def get_users_collection():
    db_conf = config.db_conf()

    client = motor.motor_asyncio.AsyncIOMotorClient(db_conf.DB_URL)
    database = client[db_conf.DB_NAME]
    users_collection = database.get_collection("users")

    return users_collection

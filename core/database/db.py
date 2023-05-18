import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()


def get_users_collection():
    db_url = os.environ.get("DB_URL")
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    database = client[str(os.environ.get("DB_NAME"))]

    users_collection = database.get_collection("users")
    return users_collection


# from pymongo.mongo_client import MongoClient
#
# client = MongoClient(os.environ.get("DB_URL"))
# database = client[str(os.environ.get("DB_NAME"))]
#
# users_collection = database.get_collection("users")

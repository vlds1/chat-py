import os

from pymongo.mongo_client import MongoClient

client = MongoClient(os.environ.get("DB_URL"))
database = client[str(os.environ.get("DB_NAME"))]

users_collection = database.get_collection("users")

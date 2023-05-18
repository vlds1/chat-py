from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb://localhost:27017/chat")
database = client.chat

users_collection = database.get_collection("users")

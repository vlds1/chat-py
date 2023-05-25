import datetime

import bcrypt
import jwt
from config import get_config
from database.db import get_users_collection


class TokenService:
    def __init__(self):
        self.config = get_config()

    async def create_token(self, user_data: dict, token_type: str, exp: int) -> str:
        payload = {
            "_id": str(user_data["_id"]),
            "email": user_data["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
            "type": token_type,
        }
        token = jwt.encode(
            payload=payload,
            key=self.config.JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return token

    async def validate_token(self, token: dict) -> dict:
        refresh_token_data = jwt.decode(
            token["refresh_token"],
            key=self.config.JWT_SECRET_KEY,
            algorithms=["HS256"],
        )
        current_datetime = datetime.datetime.utcnow()
        is_valid = current_datetime < datetime.datetime.fromtimestamp(
            refresh_token_data["exp"]
        )
        return {"is_valid": is_valid, "data": refresh_token_data}


class UserExtractorService:
    def __init__(self):
        self.users_collection = get_users_collection()

    async def get_user(self, user_data: dict) -> dict:
        user = await self.users_collection.find_one(
            filter={"email": user_data["email"]}
        )
        return user


class UserInserterService:
    def __init__(self):
        self.users_collection = get_users_collection()

    async def create_new_user(self, user_data: dict) -> dict:
        user_data["password"] = bcrypt.hashpw(
            password=user_data["password"].encode(), salt=bcrypt.gensalt(rounds=12)
        )
        user = await self.users_collection.insert_one(user_data)
        return user


class UserResponse:
    def response(self, detail: str, status_code: int) -> tuple:
        return {"detail": detail}, status_code

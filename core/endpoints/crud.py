import datetime

import bcrypt
import jwt
from jwt import InvalidSignatureError
from pydantic import ValidationError

from core.config import JWT_SECRET_KEY
from core.database.db import get_users_collection
from core.endpoints.services import create_token
from core.schemas.schemas import JWTSchema, UserSchema


class AuthUser:
    def __init__(self):
        self.users_collection = get_users_collection()

    async def create_new_user(self, user_data: dict) -> tuple:
        try:
            user_data = UserSchema(**user_data).dict()
            user_exists = await self.users_collection.find_one(
                filter={"email": user_data["email"]}
            )

            if user_exists:
                return {"detail": "user already exists"}, 409

            user_data["password"] = bcrypt.hashpw(
                password=user_data["password"].encode(), salt=bcrypt.gensalt(rounds=12)
            )
            await self.users_collection.insert_one(user_data)
            return {"detail": "user has been registered"}, 201
        except ValidationError as e:
            return {"detail": e.errors()}, 400

    async def login_user(self, user_data: dict) -> tuple:
        try:
            user_data = UserSchema(**user_data).dict()
            user_exists = await self.users_collection.find_one(
                filter={"email": user_data["email"]}
            )
            if not user_exists:
                return {"detail": "user doesnt exists"}, 400
            passwords_compare = bcrypt.checkpw(
                user_data["password"].encode(), user_exists["password"]
            )
            if not passwords_compare:
                raise ValidationError

            access_token = await create_token(user_exists, "access", 10)
            refresh_token = await create_token(user_exists, "refresh", 24 * 60)

            return {
                "data": {"access_token": access_token, "refresh_token": refresh_token}
            }, 200
        except ValidationError as e:
            return {"detail": e.__str__()}, 400

    async def update_access_token(self, refresh_token: dict) -> tuple:
        try:
            refresh_token = JWTSchema(**refresh_token).dict()
            refresh_token_data = jwt.decode(
                refresh_token["refresh_token"],
                key=JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
            current_datetime = datetime.datetime.utcnow()
            if current_datetime > datetime.datetime.fromtimestamp(
                refresh_token_data["exp"]
            ):
                return {"refresh_token": refresh_token_data}, 200

            new_access_token = await create_token(refresh_token_data, "access", 10)
            return {"access_token": new_access_token}, 201
        except (
            InvalidSignatureError,
            ValidationError,
            jwt.exceptions.DecodeError,
        ) as e:
            return {"detail": e.__str__()}, 400

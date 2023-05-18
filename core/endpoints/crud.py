import datetime

import bcrypt
import jwt
from jwt import InvalidSignatureError
from pydantic import ValidationError

from core.database.db import users_collection
from core.endpoints.services import create_token
from core.schemas.schemas import UserSchema


async def create_new_user(user_data: dict) -> dict:
    try:
        user_data = UserSchema(**user_data).dict()
        user_exists = users_collection.find_one(filter={"email": user_data["email"]})

        if user_exists:
            return {"detail": "user already exists"}, 409

        user_data["password"] = bcrypt.hashpw(
            password=user_data["password"].encode(), salt=bcrypt.gensalt(rounds=12)
        )
        users_collection.insert_one(user_data)
        return {"detail": "user has been registered"}, 201
    except ValidationError as e:
        return {"detail": e.errors()}, 400


async def login_user(user_data: dict) -> dict:
    try:
        user_data = UserSchema(**user_data).dict()
        user_exists = users_collection.find_one(filter={"email": user_data["email"]})
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
        return {"err": e.__str__()}, 400


async def update_access_token(data):
    try:
        refresh_token_data = jwt.decode(
            data["refresh_token"],
            key="b37e50cedcd3e3f1ff64f4afc0422084ae694253cf399326868e07a35f4",
            algorithms=["HS256"],
        )
        current_datetime = datetime.datetime.utcnow()
        if current_datetime > datetime.datetime.fromtimestamp(
            refresh_token_data["exp"]
        ):
            return {"refresh_token": refresh_token_data}

        new_access_token = await create_token(refresh_token_data, "access", 10)
        return {"access_token": new_access_token}, 201
    except InvalidSignatureError as e:
        return {"err": e.__str__()}, 400

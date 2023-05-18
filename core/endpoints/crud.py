import datetime

import bcrypt
import jwt
from pydantic import ValidationError

from core.database.db import users_collection
from core.endpoints.services import create_token
from core.schemas.schemas import UserSchema


async def create_new_user(user_data: dict) -> dict:
    try:
        user_data = UserSchema(**user_data).dict()
        user_exists = users_collection.find_one(filter={"email": user_data["email"]})

        if user_exists:
            return {"status": 409, "detail": "user already exists"}

        user_data["password"] = bcrypt.hashpw(
            password=user_data["password"].encode(), salt=bcrypt.gensalt(rounds=12)
        )
        users_collection.insert_one(user_data)
        return {"status": 201, "detail": "user has been registered"}
    except ValidationError as e:
        return {"status": 400, "detail": e.errors()}


async def login_user(user_data: dict) -> dict:
    try:
        user_data = UserSchema(**user_data).dict()
        user_exists = users_collection.find_one(filter={"email": user_data["email"]})
        if not user_exists:
            return {"status": 400, "detail": "user doesnt exists"}
        passwords_compare = bcrypt.checkpw(
            user_data["password"].encode(), user_exists["password"]
        )
        if not passwords_compare:
            raise ValidationError

        access_token = await create_token(user_exists, "access", 10)
        refresh_token = await create_token(user_exists, "refresh", 24 * 60)

        return {
            "status": 200,
            "data": {"access_token": access_token, "refresh_token": refresh_token},
        }
    except ValidationError as e:
        return {"status": 400, "detail": e.errors()}


async def update_access_token(data):
    refresh_token_data = jwt.decode(
        data["refresh_token"],
        key="b37e50cedcd3e3f1ff64f4afc0422084ae694253cf399326868e07a35f4",
        algorithms=["HS256"],
    )
    current_datetime = datetime.datetime.utcnow()
    if current_datetime > datetime.datetime.fromtimestamp(refresh_token_data["exp"]):
        return {"refresh_token": refresh_token_data}

    new_access_token = await create_token(refresh_token_data, "access", 10)
    return {"status": 201, "access_token": new_access_token}

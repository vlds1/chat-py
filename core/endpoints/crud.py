import bcrypt
import jwt
from jwt import InvalidSignatureError
from pydantic import ValidationError

from core.endpoints.services import (
    TokenService,
    UserExtractorService,
    UserInserterService,
)
from core.schemas.schemas import JWTSchema, UserSchema


class AuthUser:
    def __init__(self):
        self.user_extractor = UserExtractorService()
        self.user_inserter = UserInserterService()

    async def create_new_user(self, user_data: dict) -> tuple:
        try:
            user_data = UserSchema(**user_data).dict()
            user = await self.user_extractor.get_user(user_data)
            if user:
                return {"detail": "user already exists"}, 409

            await self.user_inserter.create_new_user(user_data)
            return {"detail": "user has been registered"}, 201
        except ValidationError as e:
            return {"detail": e.errors()}, 400

    async def login_user(self, user_data: dict) -> tuple:
        token = TokenService()
        try:
            user_data = UserSchema(**user_data).dict()
            user = await self.user_extractor.get_user(user_data)
            if not user:
                return {"detail": "user doesnt exists"}, 400

            passwords_compare = bcrypt.checkpw(
                user_data["password"].encode(), user["password"]
            )
            if not passwords_compare:
                raise ValidationError

            access_token = await token.create_token(user, "access", 10)
            refresh_token = await token.create_token(user, "refresh", 24 * 60)

            return {
                "data": {"access_token": access_token, "refresh_token": refresh_token}
            }, 200
        except ValidationError as e:
            return {"detail": e.__str__()}, 400


class Token:
    def __init__(self):
        self.token = TokenService()

    async def update_access_token(self, refresh_token: dict) -> tuple:
        try:
            refresh_token = JWTSchema(**refresh_token).dict()
            token = await self.token.validate_token(refresh_token)
            if not token["is_valid"]:
                return {"err": "token expired"}, 401

            new_access_token = await self.token.create_token(
                token["data"], "access", 10
            )
            return {"access_token": new_access_token}, 201
        except (
            InvalidSignatureError,
            ValidationError,
            jwt.exceptions.DecodeError,
        ) as e:
            return {"detail": e.__str__()}, 400

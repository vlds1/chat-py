from marshmallow import Schema, fields
from pydantic import BaseModel


class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str()

    class Meta:
        strict = True


class JWTSchema(BaseModel):
    refresh_token: str

from pydantic import BaseModel, EmailStr, Extra


class UserSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = Extra.forbid


class JWTSchema(BaseModel):
    refresh_token: str

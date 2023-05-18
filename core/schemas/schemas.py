from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Extra


class UserSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = Extra.forbid

from pydantic import BaseModel, EmailStr


class MessageSchema(BaseModel):
    message: str
    from_user: str
    to_user: EmailStr

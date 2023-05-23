import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt
import jwt

from core.config import get_config
from core.database.db import get_users_collection


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

    async def validate_token(self, token):
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

    async def get_user(self, user_data):
        user = await self.users_collection.find_one(
            filter={"email": user_data["email"]}
        )
        return user


class UserInserterService:
    def __init__(self):
        self.users_collection = get_users_collection()

    async def create_new_user(self, user_data):
        user_data["password"] = bcrypt.hashpw(
            password=user_data["password"].encode(), salt=bcrypt.gensalt(rounds=12)
        )
        user = await self.users_collection.insert_one(user_data)
        return user


class EmailService:
    def __init__(self):
        self.config = get_config()

    async def send_mail(self, message):
        receiver = message.headers["to_user"]
        server = await self.get_server()
        print()
        try:
            msg = await self.set_msg(self.config.EMAIL_SENDER, receiver, message)
            server.sendmail(self.config.EMAIL_SENDER, receiver, msg.as_string())
            server.quit()
            print("message sent")
        except Exception as e:
            print(f"err {e.__str__()}")

    async def set_msg(self, sender, receiver, message):
        msg = MIMEMultipart()
        user = message.headers["from_user"]
        message = message.body.decode("utf-8")
        msg["From"] = f"Chat <{sender}>"
        msg["To"] = receiver
        msg["Subject"] = "New message"
        text = f"New message by {user}: {message}"
        part = MIMEText(text, "plain")
        msg.attach(part)
        return msg

    async def get_server(self):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.config.EMAIL_SENDER, self.config.EMAIL_PASSWORD)
            return server
        except Exception as e:
            print(f"err {e.__str__()}")

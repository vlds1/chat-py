import os

from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class BaseConfig:
    def __init__(self):
        self.DB_NAME = None
        self.DB_HOST = None
        self.DB_PORT = None
        self.DB_URL = None

    def db_conf(self):
        load_dotenv()
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")
        self.DB_URL = os.environ.get("DB_URL")
        return self


class EmailConfig:
    def __init__(self):
        load_dotenv()
        self.sender = os.environ.get("EMAIL_SENDER")
        self.password = os.environ.get("EMAIL_PASSWORD")

    def get_email_config(self):
        return self


email_config = EmailConfig()
config = BaseConfig()

import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class DatabaseConfig(BaseSettings):
    class Config:
        env_file = ".env"

    DB_NAME = os.environ.get("DB_NAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_URL = os.environ.get("DB_URL")


def get_config():
    load_dotenv()
    _config = DatabaseConfig()
    return _config

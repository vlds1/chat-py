import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class DatabaseConfig(BaseSettings):
    class Config:
        env_file = ".env"

    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_URL: str


def get_config():
    load_dotenv()
    _config = DatabaseConfig()
    return _config

from dotenv import load_dotenv
from pydantic import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = ".env"

    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_URL: str

    JWT_SECRET_KEY: str


def get_config():
    load_dotenv()
    _config = Config()
    return _config

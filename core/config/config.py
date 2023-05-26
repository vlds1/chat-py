from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    RABBIT_LOGIN: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str


def get_config():
    load_dotenv()
    _settings = Settings()
    return _settings

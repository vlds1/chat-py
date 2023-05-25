from dotenv import load_dotenv
from pydantic import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = ".env"

    RABBIT_LOGIN: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str

    EMAIL_SENDER: str
    EMAIL_PASSWORD: str


def get_config():
    load_dotenv()
    _config = Config()
    return _config

import dotenv
from pydantic import BaseSettings


class AppConfig(BaseSettings):
    class Config:
        env_file = ".env"

    APP_HOST: str
    APP_PORT: str

    RABBIT_LOGIN: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str

    CHAT_ROUTING_KEY: str
    COMMAND_ROUTING_KEY: str

    FLASK_BASE_URL: str

    JWT_SECRET_KEY: str


def get_config():
    dotenv.load_dotenv()
    _config = AppConfig()
    return _config

import os

import dotenv

dotenv.load_dotenv()


class AppConfig:
    def __init__(self):
        self.host = os.environ.get("APP_HOST")
        self.port = os.environ.get("APP_PORT")


class RabbitConfig:
    def __init__(self):
        self.login = os.environ.get("RABBIT_LOGIN")
        self.password = os.environ.get("RABBIT_PASSWORD")

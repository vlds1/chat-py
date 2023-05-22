import os

import dotenv

dotenv.load_dotenv()


class AppConfig:
    def __init__(self):
        self.host = os.environ.get("APP_HOST")
        self.port = int(os.environ.get("APP_PORT"))


app_config = AppConfig()

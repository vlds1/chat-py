import os

from flask import Flask

from core.endpoints.endpoints import auth


def create_app(mongo_url="mongodb://localhost:27017/chat", db_name="chat"):
    app = Flask(__name__)
    os.environ.update(DB_URL=mongo_url)
    os.environ.update(DB_NAME=db_name)
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    return app

import os

from config import get_config
from endpoints.endpoints import auth
from flask import Flask

config = get_config()


def create_app(mongo_url=config.DB_URL, db_name="chat"):
    app = Flask(__name__)
    print(mongo_url)
    os.environ.update(DB_URL=mongo_url)
    os.environ.update(DB_NAME=db_name)
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

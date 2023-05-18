from dotenv import load_dotenv
from endpoints.endpoints import auth
from flask import Flask

config = load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/api/v1/auth")

if __name__ == "__main__":
    app.run(port=5001, debug=True)

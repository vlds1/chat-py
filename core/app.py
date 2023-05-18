from endpoints.endpoints import auth
from flask import Flask

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)

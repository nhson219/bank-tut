from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources={r"/": {"origins": "http://localhost:4000"}})
    app.config.from_object(config_by_name[config_name])
    # CORS(app, origins="*", allow_headers=[
    # "Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
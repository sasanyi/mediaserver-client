from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.common.config import Config


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config: Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config.flask_config())

    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app


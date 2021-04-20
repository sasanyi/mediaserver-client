from werkzeug.utils import cached_property

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .common.config import Config
from .common.utils import find_files_on_path_with_patterns
from tqdm import tqdm

from flask_injector import FlaskInjector

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config: Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config.flask_config())

    db.init_app(app)
    flask_bcrypt.init_app(app)
    
    from app.dependencies import configure
    FlaskInjector(app=app, modules=[configure])
    
    return app


def walk_on_files(path: str, patterns: list) -> None:
    print("Start walking on files...")
    files = find_files_on_path_with_patterns(path, patterns)
    for i, file in tqdm(enumerate(files)):
        print(i, file)
        # TODO save files to db

    print("Finished walking on files...")

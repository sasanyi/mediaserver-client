import json

from flask_injector import FlaskInjector
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from injector import Binder, singleton

from app.app import create_app, walk_on_files, db
from app.common.config import Config
from app.webservice.blueprint import blueprint


def read_config_json(file: str = "config.json") -> dict:
    with open(file, mode="r") as file:
        config = json.load(file)
        return config


def set_up_config(configfile: dict) -> Config:
    config = Config()

    config.set("web-server", "port", int(configfile["web-server"]["port"]))
    config.set("web-server", "debug", configfile["web-server"]["debug"] == 'True')

    config.set("library-watchdog", "patterns", configfile["library-watchdog"]["patterns"])
    config.set("library-watchdog", "ignore-patterns", configfile["library-watchdog"]["ignore-patterns"])
    config.set("library-watchdog", "ignore-directories", configfile["library-watchdog"]["ignore-directories"] == 'True')
    config.set("library-watchdog", "case-sensitive", configfile["library-watchdog"]["case-sensitive"] == 'True')
    config.set("library-watchdog", "path", configfile["library-watchdog"]["path"])
    config.set("library-watchdog", "recursively", configfile["library-watchdog"]["recursively"] == 'True')

    config.set("database", "type", configfile["database"]["type"])
    config.set("database", "host", configfile["database"]["host"])
    config.set("database", "port", int(configfile["database"]["port"]))
    config.set("database", "user", configfile["database"]["user"])
    config.set("database", "password", configfile["database"]["password"])
    config.set("database", "database", configfile["database"]["database"])
    config.set("database", "preserve_context_on_exception", configfile["database"]["preserve_context_on_exception"])
    config.set("database", "sqlalchemy_track_modifications", configfile["database"]["sqlalchemy_track_modifications"])

    config.set("walk-on-files", "walk-patterns", configfile["walk-on-files"]["walk-patterns"])
    config.set("walk-on-files", "path", configfile["walk-on-files"]["path"])
    config.set_configured()

    return config


def configure_di(binder: Binder) -> None:
    """Repositories"""
    from app.common.repository.user_repository import UserRepository
    from app.common.repository.file_repository import FileRepository

    binder.bind(UserRepository, to=UserRepository, scope=singleton)
    binder.bind(FileRepository, to=FileRepository, scope=singleton)

    """Services"""
    from app.webservice.service.user_service import UserService
    from app.webservice.service.file_service import FileService

    binder.bind(UserService, to=UserService, scope=singleton)
    binder.bind(FileService, to=FileService, scope=singleton)


cfg = set_up_config(read_config_json())
app = create_app(cfg)
app.register_blueprint(blueprint)

app.app_context().push()

FlaskInjector(app=app, modules=[configure_di])

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run(task):
    if task == "server":
        print("Starting web app...")
        app.run(port=cfg.config("web-server")["port"])
    elif task == "walk-on-files":
        walk_on_files(cfg.config("walk-on-files")["path"], cfg.config("walk-on-files")["walk-patterns"])


if __name__ == '__main__':
    manager.run()

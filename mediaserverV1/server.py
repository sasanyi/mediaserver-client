import os
import unittest
import json
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.app import create_app, db, walk_on_files
from app.common.config import Config


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


cfg = set_up_config(read_config_json())

app = create_app(cfg)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run(task):
    if task == "server":
        print("Starting web app...")
        app.run(host="0.0.0.0", port=cfg.config("web-server")["port"])
    elif task == "walk-on-files":
        walk_on_files(cfg.config("walk-on-files")["path"], cfg.config("walk-on-files")["walk-patterns"])


if __name__ == '__main__':
    manager.run()

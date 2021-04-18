import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from common.config import Config
from common.app import *
from deamon.watchdogevents import *
from sqlalchemy import create_engine
from common.utils import *
from common.webservice import *
from flask_socketio import SocketIO


def readConfigJson(file="config.json"):
    with open(file, mode="r") as file:
        config = json.load(file)
        return config


def setUpConfig(configfile):
    print("Setting up the server...")

    Config.set("web-server", "port", int(configfile["web-server"]["port"]))
    Config.set("web-server", "debug", configfile["web-server"]["debug"] == 'True')

    Config.set("library-watchdog", "patterns", configfile["library-watchdog"]["patterns"])
    Config.set("library-watchdog", "ignore-patterns", configfile["library-watchdog"]["ignore-patterns"])
    Config.set("library-watchdog", "ignore-directories", configfile["library-watchdog"]["ignore-directories"] == 'True')
    Config.set("library-watchdog", "case-sensitive", configfile["library-watchdog"]["case-sensitive"] == 'True')
    Config.set("library-watchdog", "path", configfile["library-watchdog"]["path"])
    Config.set("library-watchdog", "recursively", configfile["library-watchdog"]["recursively"] == 'True')

    Config.set("database", "type", configfile["database"]["type"])
    Config.set("database", "host", configfile["database"]["host"])
    Config.set("database", "port", int(configfile["database"]["port"]))
    Config.set("database", "user", configfile["database"]["user"])
    Config.set("database", "password", configfile["database"]["password"])
    Config.set("database", "database", configfile["database"]["database"])

    Config.set("startup", "walk-patterns", configfile["startup"]["walk-patterns"])

    Config.setSetted()

    print("Server configured")


def setUpDatabase():
    if not Config.isSetted():
        raise RuntimeError("Server not configured")

    engine = create_engine('{}://{}:{}@{}:{}/{}?charset=utf8'.format(Config.config("database")["type"],
                                                                        Config.config("database")["user"],
                                                                        Config.config("database")["password"],
                                                                        Config.config("database")["host"],
                                                                        Config.config("database")["port"],
                                                                        Config.config("database")["database"]),
                           connect_args={}, encoding='utf8', convert_unicode=True)

    db = Database(engine)
    App.setDb(db)


def walkOnFiles(path):
    print("Start walking on files...")

    files = findFilesInDirWithPattern(path, Config.config("startup")["walk-patterns"])

    printProgressBar(0, len(files), prefix='Progress:', suffix='Complete', length=50)

    for i, file in enumerate(files):
        saveMusicFileToDb(file)
        printProgressBar(i + 1, len(files), prefix='Progress:', suffix='Complete', length=50)


def startWatchdog():
    if not Config.isSetted():
        raise RuntimeError("Server not configured")

    config = Config.config("library-watchdog")

    print("Starting watchdog with config: " + str(config))
    patterns = config["patterns"]
    ignore_patterns = config["ignore-patterns"]
    ignore_directories = config["ignore-directories"]
    case_sensitive = config["case-sensitive"]
    path = config["path"]
    recursively = config["recursively"]

    watchdog_events = PatternMatchingEventHandler(patterns=patterns, ignore_patterns=ignore_patterns,
                                                  ignore_directories=ignore_directories, case_sensitive=case_sensitive)
    watchdog_events.on_created = on_created
    watchdog_events.on_deleted = on_deleted
    watchdog_events.on_modified = on_modified
    watchdog_events.on_moved = on_moved

    observer = Observer()
    observer.schedule(event_handler=watchdog_events, recursive=recursively, path=path)
    observer.daemon = True

    observer.start()
    print("Watchdog started...")

    return observer


def startWebService(observer=None):
    webservice.config["DEBUG"] = Config.config("web-server")["debug"]
    webservice.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'

    socketio = SocketIO(webservice)
    socketio.run(webservice, port=Config.config("web-server")["port"], host='0.0.0.0')
    stopWatchdog(observer)


def stopWatchdog(observer):
    print("Stopping watchdog...")
    observer.stop()
    observer.join()
    print("Watchdog stopped...")


def main():
    configfile = readConfigJson()
    setUpConfig(configfile)

    setUpDatabase()

    walkOnFiles(Config.config("library-watchdog")["path"])

    observer = startWatchdog()

    startWebService(observer)
    startWebService()


if __name__ == '__main__':
    main()

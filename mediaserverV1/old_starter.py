import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from app.common.config import Config
from common.app import *
from deamon.watchdogevents import *
from sqlalchemy import create_engine
from common.utils import *
from common.webservice import *
from flask_socketio import SocketIO


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

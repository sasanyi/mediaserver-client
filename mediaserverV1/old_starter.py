import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from deamon.watchdogevents import *


def startWatchdog():

    config = {}
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


def stopWatchdog(observer):
    print("Stopping watchdog...")
    observer.stop()
    observer.join()
    print("Watchdog stopped...")

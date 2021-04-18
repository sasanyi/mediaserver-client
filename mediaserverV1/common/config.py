import logging

logging.basicConfig(filename="mediaserverV1.log", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('mediaserverV1')


class Config:
    __conf = {
        "web-server": {
            "port": 8088,
            "debug": True
        },
        "library-watchdog": {
            "patterns": ["*"],
            "ignore-patterns": "",
            "ignore-directories": True,
            "case-sensitive": True,
            "path": "./",
            "recursively": True
        },
        "database": {
            "type": "mysql",
            "host": "",
            "port": 3306,
            "user": "",
            "password": "",
            "database": ""
        },
        "startup": {
            "walk-patterns": []
        }
    }
    __setters = ["web-server", "library-watchdog", "database", "startup"]
    __setted = False

    @staticmethod
    def config(name):
        return Config.__conf[name]

    @staticmethod
    def set(name, key, value):
        if name in Config.__setters and key in Config.__conf[name].keys():
            Config.__conf[name][key] = value
        else:
            raise NameError("Name not accepted in set() method")

    @staticmethod
    def isSetted():
        return Config.__setted

    @staticmethod
    def setSetted():
        Config.__setted = True

class FlaskConfig():
    DEBUG = False
    TESTING = False
    DB_SERVER = 'localhost'
    USER = 'root'
    PASSWORD = ''
    DATABASE = 'r2mediaserver'
    DRIVER = 'mysql'

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return '{}://{}:{}@{}/{}'.format(self.DRIVER, self.USER, self.PASSWORD, self.DB_SERVER, self.DATABASE)


class Config():
    __flask_config: FlaskConfig = None
    __conf = {
        "web-server": {
            "port": 8088,
            "debug": True,
            "testing": True
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
            "database": "",
            "preserve_context_on_exception": False,
            "sqlalchemy_track_modifications": False
        },
        "walk-on-files": {
            "walk-patterns": [],
            "path": "./"
        }
    }
    __setters = ["web-server", "library-watchdog", "database", "walk-on-files"]
    __configured = False

    def config(self, name: str)->dict:
        return self.__conf[name]

    def set(self, name: str, key: str, value):
        if name in Config.__setters and key in Config.__conf[name].keys():
            self.__conf[name][key] = value
        else:
            raise NameError("Name not accepted in set() method")

    def is_configured(self):
        return self.__configured

    def set_configured(self):
        self.__configured = True

    def flask_config(self) -> FlaskConfig:
        if self.__flask_config:
            return self.__flask_config
        else:
            if not self.__configured:
                raise RuntimeError("Application not configured yet!")

            conf = FlaskConfig()
            conf.DRIVER = Config.__conf["database"]["type"]
            conf.USER = Config.__conf["database"]["user"]
            conf.PASSWORD = Config.__conf["database"]["password"]
            conf.DB_SERVER = Config.__conf["database"]["host"]
            conf.DATABASE = Config.__conf["database"]["database"]
            conf.PRESERVE_CONTEXT_ON_EXCEPTION = Config.__conf["database"]["preserve_context_on_exception"]
            conf.SQLALCHEMY_TRACK_MODIFICATIONS = Config.__conf["database"]["sqlalchemy_track_modifications"]
            conf.DEBUG = Config.__conf["web-server"]["debug"]
            conf.TESTING = Config.__conf["web-server"]["testing"]
            Config.__flask_config = conf

            return conf

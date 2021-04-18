from sqlalchemy.orm import sessionmaker
from .models import Base


class App:
    __db = None

    @staticmethod
    def setDb(db):
        App.__db = db

    @staticmethod
    def getDb():
        if App.__db is not None:
            return App.__db
        else:
            raise RuntimeError("Server not configured")


class Database:
    engine = None
    _db = None

    def __init__(self, engine):
        self.engine = engine

        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self._db = Session()

    @property
    def db(self):
        return self._db

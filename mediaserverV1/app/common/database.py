class Database(object):
    _db = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, db):
        self._db = db
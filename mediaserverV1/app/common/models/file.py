from app.app import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from .meta import Meta
import re


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), nullable=False, unique=True)

    meta_id = db.Column(db.ForeignKey("meta.id"))
    meta = db.relationship(Meta, foreign_keys=[meta_id])

    CREATEDON = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    UPDATEON = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    @hybrid_property
    def real_path(self):
        return re.sub(r'\\(.)', r'\1', self.path)

    @real_path.setter
    def real_path(self, value):
        self.path = re.escape(value)

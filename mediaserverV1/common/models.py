from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
import re
from marshmallow import Schema, fields

Base = declarative_base()


class Meta(Base):
    __tablename__ = "metas"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    date = Column(Text)
    album = Column(Text)
    genre = Column(Text)

    CREATEDON = Column(DateTime, nullable=False, default=datetime.datetime.now)
    UPDATEON = Column(DateTime, onupdate=datetime.datetime.now)


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(String(500), nullable=False, unique=True)

    meta_id = Column(ForeignKey("metas.id"))
    meta = relationship("Meta", foreign_keys=[meta_id])

    CREATEDON = Column(DateTime, nullable=False, default=datetime.datetime.now)
    UPDATEON = Column(DateTime, onupdate=datetime.datetime.now)

    @hybrid_property
    def real_path(self):
        return re.sub(r'\\(.)', r'\1', self.path)


class MetaSchema(ModelSchema):
    album = fields.Str()
    artist = fields.Str()
    title = fields.Str()
    date = fields.Str()
    genre = fields.Str()


class FileSchema(ModelSchema):
    class Meta:
        model = File

    meta = fields.Nested(MetaSchema)
    real_path = fields.Function(lambda obj: re.sub(r'\\(.)', r'\1', obj.path))

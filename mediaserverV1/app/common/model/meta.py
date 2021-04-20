from ...app import db
import datetime


class Meta(db.Model):
    __tablename__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    artist = db.Column(db.Text)
    date = db.Column(db.Text)
    album = db.Column(db.Text)
    genre = db.Column(db.Text)

    CREATEDON = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    UPDATEON = db.Column(db.DateTime, onupdate=datetime.datetime.now)

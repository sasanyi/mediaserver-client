from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from sqlalchemy.exc import SQLAlchemyError

from common.models import *
from common.app import App
from sqlalchemy.sql.expression import update
import re
from common.config import logger
import os


def on_created(event):
    print(f"{event.src_path} has been created!")
    db = App.getDb().db
    file_check = db.query(File).where(File.path == re.escape(os.path.abspath(event.src_path))).one_or_none()
    if not file_check:
        file = File(path=re.escape(os.path.abspath(event.src_path)), meta=Meta())
        db.add(file)
        db.commit()

    try:
        audio = EasyID3(event.src_path)
    except:
        print("No metadatas in this file")
    else:
        updateMeta(event.src_path, audio)


def on_deleted(event):
    print(f"{event.src_path} has been deleted!")
    db = App.getDb().db
    file = db.query(File).where(File.path == re.escape(os.path.abspath(event.src_path))).one_or_none()
    if file:
        db.delete(file.meta)
        db.delete(file)
        db.commit()


def on_modified(event):
    print(f"{event.src_path} has been modified")
    db = App.getDb().db
    file = db.query(File).filter(File.path == re.escape(os.path.abspath(event.src_path))).one_or_none()
    if file:
        try:
            audio = EasyID3(event.src_path)
        except:
            print("No metadatas in this file")
        else:
            updateMeta(event.src_path, audio)
    else:
        on_created(event)


def on_moved(event):
    print(f"{event.src_path} has been moved to {event.dest_path}")
    db = App.getDb().db
    file = db.query(File).where(File.path == re.escape(os.path.abspath(event.src_path))).one_or_none()
    if file:
        file.path = re.escape(os.path.abspath(event.dest_path))
        db.commit()


def updateMeta(path, audio):
    db = App.getDb().db
    file = db.query(File).filter(File.path == re.escape(os.path.abspath(path))).one_or_none()
    meta = file.meta
    if file:
        for key in audio.keys():
            setattr(meta, key, audio[key])
            if (type(audio[key]) is list):
                setattr(meta, key, ",".join(audio[key]))

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(str(type(e)) + " - " + str(e) + " - " + path)

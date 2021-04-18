import json

from common.app import App
from common.models import *
from flask import flash, redirect, render_template, \
    request, url_for, Response
from mutagen.easyid3 import EasyID3


def index():
    return render_template("index.html")


def show_all_musics():
    return render_template("musics.html")


def get_all_musics():
    db = App.getDb().db
    musics = db.query(File).all()
    musics_schema = FileSchema(many=True)
    return {"musics": musics_schema.dump(musics)}


def edit_music_view(id: int):
    db = App.getDb().db
    music = db.query(File).filter(File.id == id).one_or_none()
    if music:
        return render_template("music-edit.html", music=music)
    else:
        flash('Nem található ilyen file!', 'danger')
        return redirect(url_for('show_all_musics'))


def edit_music(id: int):
    db = App.getDb().db
    music = db.query(File).filter(File.id == id).one_or_none()
    if music:
        music.meta.title = request.form['title']
        music.meta.artist = request.form['artist']
        music.meta.album = request.form['album']
        music.meta.date = request.form['date']
        music.meta.genre = request.form['genre']

        db.commit()

        audio = EasyID3(music.real_path)
        audio["title"] = request.form['title']
        audio["artist"] = request.form['artist']
        audio["album"] = request.form['album']
        audio["date"] = request.form['date']
        audio["genre"] = request.form['genre']

        audio.save()

        flash('Sikeresen átírtad a metaadatokat!', 'success')

        return redirect(url_for('edit_music_view', id=id))
    else:
        flash('Nem található ilyen file!', 'danger')
        return redirect(url_for('show_all_musics'))

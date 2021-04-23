import re

from injector import inject
from mutagen import MutagenError
from mutagen.easyid3 import EasyID3

from app.common.repositories.file_repository import FileRepository
from app.common.utils import NoPublicConstructor
from app.common.models.file import File
from app.common.models.meta import Meta


class MusicFileMetaData(metaclass=NoPublicConstructor):
    def __init__(self):
        self.music_file = None
        self.file_repository = None
        self.path = None

    @classmethod
    @inject
    def load(cls, path: str, file_repository: FileRepository):
        instance = cls._create()
        instance.music_file = EasyID3(path)
        instance.file_repository = file_repository
        instance.path = re.escape(path)
        return instance

    @property
    def title(self):
        return self.music_file['title']

    @title.setter
    def title(self, value):
        self.music_file["title"] = value

    @property
    def artist(self):
        return self.music_file['artist']

    @artist.setter
    def artist(self, value):
        self.music_file["artist"] = value

    @property
    def date(self) -> str:
        return self.music_file['date']

    @date.setter
    def date(self, value: str):
        self.music_file["date"] = value

    @property
    def album(self) -> str:
        return self.music_file['album']

    @album.setter
    def album(self, value: str):
        self.music_file["album"] = value

    @property
    def genre(self) -> str:
        return self.music_file['genre']

    @genre.setter
    def genre(self, value: str):
        self.music_file["genre"] = value

    def update_with_dict(self, metas: dict):
        for key in metas:
            setattr(self, key, metas[key])

    def get_metas(self) -> dict:
        return {"title": self.title, "artist": self.artist, "date": self.date, "album": self.album,
                "genre": self.genre}

    def commit(self):
        try:
            self.music_file.save()
            music_from_db = self.file_repository.get_file_by_path(path=self.path)
            if music_from_db:
                meta_datas = self.get_metas()
                for key in meta_datas:
                    setattr(music_from_db.meta, key, meta_datas[key])
                self.file_repository.save_changes(music_from_db)
            else:
                new_file = File()
                new_file.path = self.path
                new_file.meta = Meta()

                meta_datas = self.get_metas()
                for key in meta_datas:
                    setattr(new_file.meta, key, meta_datas[key])

                self.file_repository.save_changes(new_file)

        except MutagenError as e:
            print(e)

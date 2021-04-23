from app.app import db
from app.common.models.file import File


class FileRepository:
    def get_all_files(self) -> list:
        return File.query.all()

    def get_file_by_path(self, path: str):
        return File.query.filter_by(path=path).first()

    def save_changes(self, data: File):
        db.session.add(data)
        db.session.commit()

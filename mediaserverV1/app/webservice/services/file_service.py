from injector import inject
from app.common.repositories.file_repository import FileRepository


class FileService(object):

    @inject
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def get_all_files(self) -> list:
        return self.file_repository.get_all_files()

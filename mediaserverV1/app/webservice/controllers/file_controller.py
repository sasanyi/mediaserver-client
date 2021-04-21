from flask import request
from flask_restplus import Resource
from injector import inject
from app.webservice.dtos.meta_dto import MetaDto
from app.webservice.dtos.file_dto import FileDto

from app.webservice.services.file_service import FileService

meta_api = MetaDto.api
file_api = FileDto.api

_meta = MetaDto.meta
_file = FileDto.file


@file_api.route('/')
class FileRoot(Resource):
    @inject
    def __init__(self, file_service: FileService, api):
        super().__init__(api)
        self.file_service = file_service

    @file_api.doc('lsit all music from library')
    @file_api.marshal_list_with(_file)
    def get(self):
        return self.file_service.get_all_files()

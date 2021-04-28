from flask_restx import Namespace, fields
from app.webservice.dtos.meta_dto import MetaDto


class FileDto:
    api = Namespace('file', description='file related operations')
    file = api.model('file', {
        'real_path': fields.String(required=False, description='path of music on server'),
        'meta': fields.Nested(MetaDto.meta)
    })

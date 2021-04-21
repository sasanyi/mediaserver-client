from flask_restplus import Namespace, fields


class MetaDto:
    api = Namespace('meta', description='meta related operations')
    meta = api.model('meta', {
        'title': fields.String(required=False, description='title of music'),
        'artist': fields.String(required=False, description='artist of music'),
        'date': fields.String(required=False, description='date of music'),
        'album': fields.String(required=False, description='album of music'),
        'genre': fields.String(required=False, description='genre of music')
    })

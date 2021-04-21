from flask_restplus import Api
from flask import Blueprint

from .controller.user_controller import api as user_ns
from .controller.file_controller import meta_api as meta_ns
from .controller.file_controller import file_api as file_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='MediaServerV1',
          version='1.0',
          description='Rest API for media servere'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(meta_ns)
api.add_namespace(file_ns, path='/music')

from flask import request
from flask_restx import Resource
from injector import inject

from app.webservice.dtos.user_dto import UserDto
from app.webservice.services.user_service import UserService

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserRoot(Resource):
    @inject
    def __init__(self, user_service: UserService, api):
        super().__init__(api)
        self.user_service = user_service

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user)
    def get(self):
        """List all registered users"""
        return self.user_service.get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        if self.user_service.save_new_user(data):
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class UserFindById(Resource):
    @inject
    def __init__(self, user_service: UserService, api):
        super().__init__(api)
        self.user_service = user_service

    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = self.user_service.get_user_by_id(public_id)
        if not user:
            api.abort(404)
        else:
            return user

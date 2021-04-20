from flask import request
from flask_restplus import Resource
from injector import inject

from ..dto.user_dto import UserDto
from ..service.user_service import UserService

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
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
        print(data)
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

from injector import inject

from app.common.repositories.user_repository import UserRepository
from app.common.models.user import User

import uuid
import datetime


class UserService(object):

    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save_new_user(self, user: dict) -> bool:
        user_find = self.user_repository.get_user_by_email(email=user["email"])
        if not user_find:
            new_user = User()
            new_user.public_id = str(uuid.uuid4())
            new_user.email = user["email"]
            new_user.username = user["username"]
            new_user.password = user['password']
            new_user.registered_on = datetime.datetime.utcnow()

            self.user_repository.create_user(new_user)
            return True
        return False

    def get_user_by_id(self, id: str) -> User:
        return self.user_repository.get_user_by_id(id)

    def get_all_users(self) -> list:
        return self.user_repository.get_all_users()

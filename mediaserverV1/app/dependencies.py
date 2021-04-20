from injector import singleton, Binder
from .common.repository.user_repository import UserRepository


def configure(binder: Binder):
    binder.bind(UserRepository, to=UserRepository, scope=singleton)

from _pytest.fixtures import fixture
import pytest

from flask_injector import FlaskInjector
from injector import Binder, singleton

from app.app import create_app
from app.common.config import Config, FlaskConfig
from app.common.models.user import User
from app.webservice.blueprint import blueprint
from app.webservice.services.user_service import UserServiceAbstract, UserService


@fixture
def user_service_mock(get_all_users_fixture):
    class UserServiceMock(UserServiceAbstract):
        def save_new_user(self, user: dict) -> bool:
            pass

        def get_user_by_id(self, id: str) -> User:
            pass

        def get_all_users(self) -> list:
            return get_all_users_fixture()
    
    yield UserServiceMock


class TestConfig:
    def flask_config(self) -> FlaskConfig:
        return FlaskConfig()


@pytest.fixture(scope="session")
def test_config() -> Config:
    yield TestConfig()


@pytest.fixture
def test_modules(user_service_mock) -> callable:
    def test_binder(binder: Binder):
        binder.bind(UserService, to=user_service_mock, scope=singleton)

    yield test_binder


@pytest.fixture
def client(test_config, test_modules):
    """A test client for the app."""
    app = create_app(test_config)
    app.register_blueprint(blueprint)
    FlaskInjector(app=app, modules=[test_modules])
    yield app.test_client()

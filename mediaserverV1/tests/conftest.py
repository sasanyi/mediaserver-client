from flask.app import Flask
import pytest

from flask_injector import FlaskInjector
from sqlalchemy.orm import Session
from injector import Binder, singleton

from app.app import create_app, db
from app.common.config import FlaskConfig
from app.common.repositories.user_repository import UserRepository
from app.webservice.blueprint import blueprint
from app.webservice.services.user_service import UserService

from tests.factories import *


class TestConfig:
    def flask_config(self) -> FlaskConfig:
        return FlaskConfig("mediaserver-mysql", "admin", "admin")


@pytest.fixture(scope="session")
def test_modules() -> callable:
    def _test_modules(binder: Binder):
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(UserService, to=UserService, scope=singleton)
    
    yield _test_modules


@pytest.fixture(scope="session")
def app(test_modules: callable) -> Flask:
    app = create_app(TestConfig())
    app.register_blueprint(blueprint)
    app.app_context().push()
    FlaskInjector(app=app, modules=[test_modules])

    yield app


@pytest.fixture(scope="session")
def manage_tables(app: Flask):
    app.app_context().push()
    db.create_all()

    yield

    db.drop_all()


@pytest.fixture
def session(manage_tables: None) -> Session:
    """Returns an sqlalchemy session"""

    db.session.commit()
    yield db.session()
    db.session.rollback()
    db.session.close_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    yield app.test_client()

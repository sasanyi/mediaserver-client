import pytest
from flask.app import Flask
from flask.testing import FlaskClient
from flask_injector import FlaskInjector
from injector import Binder, singleton
from sqlalchemy.orm.session import Session, close_all_sessions

from app.app import create_app, db
from app.common.config import FlaskConfig
from app.common.repositories.user_repository import UserRepository
from app.webservice.blueprint import blueprint
from app.webservice.services.user_service import UserService

from tests.factories import *


def clear_data(session):
    for table in reversed(db.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


class TestConfig:
    def flask_config(self) -> FlaskConfig:
        return FlaskConfig(db_server="mediaserver-mysql", user="admin", password="admin")


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
    session = db.session()
    
    yield session
    
    clear_data(session)
    close_all_sessions()


@pytest.fixture
def client(app) -> FlaskClient:
    """A test client for the app."""
    yield app.test_client()

import datetime as dt

import pytest
from app.common.models.user import User
from tests.defaults import EMAIL_ADDRESS, PASSWORD_HASH, PUBLIC_ID, USERNAME


@pytest.fixture
def user_factory():
    def _user_factory(**kwargs) -> User:
        user = User()
        if "id" in kwargs:
            user.id = kwargs["id"]
        user.email = kwargs.get("email", EMAIL_ADDRESS)
        user.registered_on = kwargs.get("registered_on", dt.datetime.utcnow())
        user.admin = kwargs.get("admin", False)
        user.public_id = kwargs.get("public_id", PUBLIC_ID)
        user.username = kwargs.get("username", USERNAME)
        user.password_hash = kwargs.get("password_hash", PASSWORD_HASH)

        return user
    
    yield _user_factory

import datetime as dt
from pytest import fixture
from app.common.models.user import User

EMAIL_ADDRESS = "sample@email.hu"
USERNAME = "Mr Sample"
PASSWORD_HASH = "0123456789"
PUBLIC_ID = "1"


def user_factory(**kwargs) -> User:
    user = User()
    user.id = kwargs.get("id", 1)
    user.email = kwargs.get("email", EMAIL_ADDRESS)
    user.registered_on = kwargs.get("registered_on", dt.datetime.utcnow())
    user.admin = kwargs.get("admin", False)
    user.public_id = kwargs.get("public_id", PUBLIC_ID)
    user.username = kwargs.get("username", USERNAME)
    user.password_hash = kwargs.get("password_hash", PASSWORD_HASH)

    return user


@fixture
def get_all_users_fixture():
    yield lambda: [user_factory()]


class TestUserController:
    def test_get_controller_returns_the_expected_user(self, client):
        expected_response = [
            {
                "email": EMAIL_ADDRESS,
                "username": USERNAME,
                "password": None,
                "public_id": PUBLIC_ID
            }
        ]

        response = client.get("/user/")
        assert response.json == expected_response

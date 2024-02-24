from sqlalchemy.orm import Session

from app.common.models.user import User
from app.common.repositories.user_repository import UserRepository
from app.webservice.services.user_service import UserService
from tests.defaults import EMAIL_ADDRESS, PASSWORD_HASH, PUBLIC_ID, USERNAME


class TestUserServiceSaveNewUser:
    def test_inserts_new_user_via_user_repository(self, session: Session):
        test_data = {
            "email": EMAIL_ADDRESS,
            "username": USERNAME,
            "password": PASSWORD_HASH,
            "public_id": PUBLIC_ID,
        }

        response = UserService(UserRepository()).save_new_user(test_data)
        assert session.query(User).count() == 1
        assert response is True

    def test_inserts_new_user_responds_false_if_the_user_is_existed(self, session: Session, user_factory: callable):
        session.add(user_factory())

        test_data = {
            "email": EMAIL_ADDRESS,
            "username": USERNAME,
            "password": PASSWORD_HASH,
            "public_id": PUBLIC_ID,
        }

        UserService(UserRepository())
        response = UserService(UserRepository()).save_new_user(test_data)
        assert session.query(User).count() == 1
        assert response is False

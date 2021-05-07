from sqlalchemy.orm import Session
from app.common.models.user import User
from app.common.repositories.user_repository import UserRepository
from tests.defaults import EMAIL_ADDRESS, PASSWORD_HASH, PUBLIC_ID, USERNAME


class TestUserRepositoryCreateUser:
    def test_inserts_new_user_record_with_the_given_user_model(self, session: Session, user_factory: callable):
        test_user = user_factory()
        UserRepository().create_user(test_user)

        user = session.query(User).one()
        assert user.email == EMAIL_ADDRESS
        assert user.username == USERNAME
        assert user.password_hash == PASSWORD_HASH
        assert user.public_id == PUBLIC_ID


class TestUserRepositoryGetAllUsers:
    OTHER_EMAIL_ADDRESS = "other_email@email.hu"
    OTHER_USERNAME = "other_username"
    OTHER_PUBLIC_ID = "69"

    def test_retreives_all_users(self, session: Session, user_factory: callable):
        test_user = user_factory()
        test_other_user = user_factory(
            email=self.OTHER_EMAIL_ADDRESS, username=self.OTHER_USERNAME, public_id=self.OTHER_PUBLIC_ID
        )
        expected_users = [test_user, test_other_user]
        session.add_all(expected_users)

        assert UserRepository().get_all_users() == expected_users

    def test_retreives_empty_list_if_there_is_no_users(self):
        assert UserRepository().get_all_users() == []


class TestUserRepositoryGetUserById:
    def test_returns_the_user_for_the_given_id(self, session: Session, user_factory: callable):
        test_user = user_factory()
        session.add(test_user)

        assert UserRepository().get_user_by_id(PUBLIC_ID) == test_user

    def test_returns_None_if_there_is_no_users_to_the_given_public_id(
        self, session: Session, user_factory: callable
    ):
        test_user = user_factory()
        session.add(test_user)

        assert UserRepository().get_user_by_id(69) is None


class TestUserRepositoryGetUserByEmail:
    def test_returns_the_user_for_the_given_email(self, session: Session, user_factory: callable):
        test_user = user_factory()
        session.add(test_user)

        assert UserRepository().get_user_by_email(EMAIL_ADDRESS) == test_user

    def test_returns_None_if_there_is_no_users_to_the_given_public_email(
        self, session: Session, user_factory: callable
    ):
        test_user = user_factory()
        session.add(test_user)

        assert UserRepository().get_user_by_email("other_email@email.hu") is None

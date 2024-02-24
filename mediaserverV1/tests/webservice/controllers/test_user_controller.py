from http import HTTPStatus
import pytest
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from app.common.models.user import User
from tests.defaults import EMAIL_ADDRESS, PASSWORD_HASH, USERNAME, PUBLIC_ID

USER_URL = "/user/"


@pytest.mark.usefixtures("manage_tables")
class TestGetUserController:
    def test_returns_empty_list_if_there_are_no_users(self, client: FlaskClient):
        response = client.get(USER_URL)
        assert response.json == []

    def test_returns_the_expected_user(self, client: FlaskClient, session: Session, user_factory: callable):
        session.add(user_factory())

        expected_response = [
            {
                "email": EMAIL_ADDRESS,
                "username": USERNAME,
                "password": None,
                "public_id": PUBLIC_ID
            }
        ]

        response = client.get(USER_URL)
        assert response.json == expected_response


@pytest.mark.usefixtures("manage_tables")
class TestPostUserContoller:
    def test_inserts_new_user_record_into_table_with_given_values(self, client: FlaskClient, session: Session):
        test_body = {
            "email": EMAIL_ADDRESS,
            "username": USERNAME,
            "password": PASSWORD_HASH,
            "public_id": PUBLIC_ID,
        }

        response = client.post(USER_URL, json=test_body)

        assert session.query(User).count() == 1
        assert response.json == {'status': 'success', 'message': 'Successfully registered.'}
        assert response.status_code == HTTPStatus.CREATED

    def test_responses_conflict_because_the_user_is_already_existed(
        self, client: FlaskClient, session: Session, user_factory: callable
    ):
        session.add(user_factory())

        test_body = {
            "email": EMAIL_ADDRESS,
            "username": USERNAME,
            "password": PASSWORD_HASH,
            "public_id": PUBLIC_ID,
        }

        response = client.post(USER_URL, json=test_body)

        assert session.query(User).count() == 1
        assert response.json == {'status': 'fail', 'message': 'User already exists. Please Log in.'}
        assert response.status_code == HTTPStatus.CONFLICT

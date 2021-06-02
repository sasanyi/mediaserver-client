import pytest
from tests.defaults import EMAIL_ADDRESS, USERNAME, PUBLIC_ID


@pytest.mark.usefixtures("manage_tables")
class TestUserController:
    def test_get_controller_returns_empty_list_if_there_are_no_users(self, client):
        response = client.get("/user/")
        assert response.json == []

    def test_get_controller_returns_the_expected_user(self, client, session, user_factory):
        session.add(user_factory())

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

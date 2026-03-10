import pytest


@pytest.mark.django_db
def test_get_me(api_client, user):
    api_client.force_authenticate(user)

    response = api_client.get("/api/users/me/")

    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_me_requires_auth(api_client):
    response = api_client.get("/api/users/me/")
    assert response.status_code == 401

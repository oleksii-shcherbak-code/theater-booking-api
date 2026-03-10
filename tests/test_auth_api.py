import pytest


@pytest.mark.django_db
def test_login_success(api_client, user):
    response = api_client.post("/api/auth/login/", {
        "email": "user@test.com",
        "password": "test1234"
    })

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password(api_client, user):
    response = api_client.post("/api/auth/login/", {
        "email": "user@test.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401

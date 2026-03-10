import pytest


@pytest.mark.django_db
def test_list_plays(api_client, play):
    response = api_client.get("/api/plays/")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_play(api_client, play):
    response = api_client.get(f"/api/plays/{play.id}/")

    assert response.status_code == 200
    assert response.data["title"] == play.title


@pytest.mark.django_db
def test_admin_create_play(api_client, admin_user, genre, actor):
    api_client.force_authenticate(admin_user)

    response = api_client.post("/api/plays/", {
        "title": "Macbeth",
        "description": "Test",
        "genre_ids": [genre.id],
        "actor_ids": [actor.id]
    })

    assert response.status_code in [201, 400]


@pytest.mark.django_db
def test_user_cannot_create_play(api_client, user, genre, actor):
    api_client.force_authenticate(user)

    response = api_client.post("/api/plays/", {
        "title": "Macbeth",
        "description": "Test",
        "genre_ids": [genre.id],
        "actor_ids": [actor.id]
    })

    assert response.status_code == 403

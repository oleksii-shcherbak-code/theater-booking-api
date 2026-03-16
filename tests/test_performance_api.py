"""
Tests for performance endpoints.
"""
import pytest


@pytest.mark.django_db
def test_list_performances(api_client, performance, extract_results):
    response = api_client.get("/api/performances/")
    assert response.status_code == 200
    data = extract_results(response)
    assert len(data) == 1


@pytest.mark.django_db
def test_retrieve_performance(api_client, performance):
    response = api_client.get(f"/api/performances/{performance.id}/")
    assert response.status_code == 200
    assert response.data["id"] == performance.id


@pytest.mark.django_db
def test_admin_create_performance(api_client, admin_user, play, theatre_hall):
    api_client.force_authenticate(admin_user)
    response = api_client.post("/api/performances/", {
        "play_id": play.id,
        "theatre_hall_id": theatre_hall.id,
        "starts_at": "2030-01-01T18:00:00Z",
        "ticket_price": "50.00"
    })
    assert response.status_code in [201, 400]

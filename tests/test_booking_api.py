import pytest
from booking.models import Booking, Ticket


@pytest.mark.django_db
def test_create_booking(api_client, user):
    api_client.force_authenticate(user)

    response = api_client.post("/api/bookings/")

    assert response.status_code == 201
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_list_user_bookings(api_client, user, booking):
    api_client.force_authenticate(user)

    response = api_client.get("/api/bookings/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_ticket(api_client, user, performance, booking):
    api_client.force_authenticate(user)

    response = api_client.post(
        f"/api/bookings/{booking.id}/add_ticket/",
        {
            "performance_id": performance.id,
            "row": 1,
            "seat": 1
        }
    )

    assert response.status_code in [201, 400]


@pytest.mark.django_db
def test_confirm_booking(api_client, user, booking):
    api_client.force_authenticate(user)

    response = api_client.post(
        f"/api/bookings/{booking.id}/confirm/"
    )

    assert response.status_code == 200

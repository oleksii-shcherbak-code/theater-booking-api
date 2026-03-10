import pytest

from booking.models import Booking


@pytest.mark.django_db
def test_user_cannot_access_other_booking(api_client, user, admin_user):
    booking = Booking.objects.create(user=admin_user)

    api_client.force_authenticate(user)

    response = api_client.get(f"/api/bookings/{booking.id}/")

    assert response.status_code in [403, 404]


@pytest.mark.django_db
def test_booking_requires_auth(api_client):
    response = api_client.get("/api/bookings/")
    assert response.status_code == 401

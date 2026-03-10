import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from plays.models import Play, Genre, Actor
from schedule.models import TheatreHall, Performance
from booking.models import Booking

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@test.com",
        password="test1234"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@test.com",
        password="test1234"
    )


@pytest.fixture
def genre(db):
    return Genre.objects.create(name="Drama")


@pytest.fixture
def actor(db):
    return Actor.objects.create(first_name="Tom", last_name="Hardy")


@pytest.fixture
def play(db, genre, actor):
    play = Play.objects.create(
        title="Hamlet",
        description="Test description"
    )
    play.genres.add(genre)
    play.actors.add(actor)
    return play


@pytest.fixture
def theatre_hall(db):
    return TheatreHall.objects.create(
        name="Main hall",
        rows=10,
        seats_per_row=10
    )


@pytest.fixture
def performance(db, play, theatre_hall):
    return Performance.objects.create(
        play=play,
        theatre_hall=theatre_hall,
        starts_at="2030-01-01T18:00:00Z",
        ticket_price=50
    )


@pytest.fixture
def booking(db, user):
    return Booking.objects.create(user=user)

from django.db import transaction
import logging
from plays.models import Play
from typing import Iterable

logger = logging.getLogger(__name__)


def create_play(*, title: str, description: str, genres: Iterable, actors: Iterable) -> Play:
    """
    Create a new play with given title, description, genres and actors.
    """
    with transaction.atomic():
        play = Play.objects.create(
            title=title,
            description=description,
        )
        play.genres.set(genres)
        play.actors.set(actors)
    logger.info("Created play %s", play.pk)
    return play


def update_play(*, play: Play, title: str, description: str, genres: Iterable, actors: Iterable) -> Play:
    """
    Update an existing play with new title, description, genres and actors.
    """
    with transaction.atomic():
        play.title = title
        play.description = description
        play.save(update_fields=("title", "description"))
        play.genres.set(genres)
        play.actors.set(actors)
    logger.info("Updated play %s", play.pk)
    return play

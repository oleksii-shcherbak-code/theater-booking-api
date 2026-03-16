from django.db import transaction
import logging
from schedule.models import Performance, TheatreHall
from plays.models import Play
from django.utils import timezone
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def create_performance(
    *,
    play: Play,
    theatre_hall: TheatreHall,
    starts_at,
    ticket_price,
) -> Performance:
    """
    Create a new performance for a play in a theatre hall at a given time and price.
    """
    if starts_at < timezone.now():
        raise ValidationError("starts_at cannot be in the past.")
    with transaction.atomic():
        performance = Performance.objects.create(
            play=play,
            theatre_hall=theatre_hall,
            starts_at=starts_at,
            ticket_price=ticket_price,
        )
    logger.info("Created performance %s", performance.pk)
    return performance

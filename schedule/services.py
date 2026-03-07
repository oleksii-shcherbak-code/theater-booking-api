"""
Service layer for schedule domain.

Contains business logic for creating and managing performances.
"""

from schedule.models import Performance


def create_performance(
    *,
    play,
    theatre_hall,
    starts_at,
    ticket_price,
) -> Performance:
    """
    Create a new performance.

    Args:
        play: Play instance.
        theatre_hall: TheatreHall instance.
        starts_at: Performance start datetime.
        ticket_price: Ticket price.

    Returns:
        Created Performance instance.
    """
    return Performance.objects.create(
        play=play,
        theatre_hall=theatre_hall,
        starts_at=starts_at,
        ticket_price=ticket_price,
    )

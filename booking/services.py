"""
Service layer for booking domain.

Contains business logic for booking flow.
"""

from django.db import transaction
from django.core.exceptions import ValidationError

from booking.models import Booking, Ticket
from schedule.models import Performance


def create_booking(*, user) -> Booking:
    """
    Create a new booking (cart) for user.
    """
    return Booking.objects.create(user=user)


@transaction.atomic
def add_ticket_to_booking(
    *,
    booking: Booking,
    performance: Performance,
    row: int,
    seat: int,
) -> Ticket:
    """
    Add ticket to booking with seat locking.
    """
    existing_ticket = (
        Ticket.objects
        .select_for_update()
        .filter(
            performance=performance,
            row=row,
            seat=seat,
        )
        .first()
    )

    if existing_ticket:
        raise ValidationError("Seat is already booked.")

    return Ticket.objects.create(
        booking=booking,
        performance=performance,
        row=row,
        seat=seat,
    )


@transaction.atomic
def confirm_booking(*, booking: Booking) -> Booking:
    """
    Confirm booking.
    """
    booking.is_confirmed = True
    booking.save(update_fields=("is_confirmed",))
    return booking

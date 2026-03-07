"""
Service layer for booking domain.

Contains business logic for booking flow.
"""

from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError

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
    Add ticket to booking.

    Protected by DB-level unique constraint.
    """
    if booking.is_confirmed:
        raise ValidationError("Cannot modify confirmed booking.")

    try:
        return Ticket.objects.create(
            booking=booking,
            performance=performance,
            row=row,
            seat=seat,
        )
    except IntegrityError:
        raise ValidationError("Seat is already booked.")


@transaction.atomic
def confirm_booking(*, booking: Booking) -> Booking:
    """
    Confirm booking.
    """
    if booking.is_confirmed:
        raise ValidationError("Booking is already confirmed.")

    booking.is_confirmed = True
    booking.save(update_fields=("is_confirmed",))
    return booking

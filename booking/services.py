import logging

from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from booking.models import Booking, Ticket
from schedule.models import Performance

logger = logging.getLogger(__name__)


def create_booking(*, user) -> Booking:
    """
    Create a new booking for the given user.
    """
    booking = Booking.objects.create(user=user)
    logger.info("Created booking %s for user %s", booking.pk, getattr(user, "pk", None))
    return booking


@transaction.atomic
def add_ticket_to_booking(
    *,
    booking: Booking,
    performance: Performance,
    row: int,
    seat: int,
) -> Ticket:
    """
    Add a ticket to the booking while locking the booking row and performance to avoid races.
    """
    booking = Booking.objects.select_for_update().get(pk=booking.pk)
    if booking.is_confirmed:
        raise ValidationError("Cannot modify confirmed booking.")
    performance = Performance.objects.select_for_update().get(pk=performance.pk)
    if row < 1 or seat < 1:
        raise ValidationError("Row and seat must be greater than 0.")
    theatre_hall = getattr(performance, "theatre_hall", None)
    if theatre_hall:
        if row > theatre_hall.rows:
            raise ValidationError("Row is out of theatre hall bounds.")
        if seat > theatre_hall.seats_per_row:
            raise ValidationError("Seat is out of theatre hall bounds.")
    try:
        ticket = Ticket.objects.create(
            booking=booking,
            performance=performance,
            row=row,
            seat=seat,
        )
        logger.info("Added ticket %s to booking %s", ticket.pk, booking.pk)
        return ticket
    except IntegrityError:
        logger.exception("IntegrityError when adding ticket to booking %s", booking.pk)
        raise ValidationError("Seat is already booked.")


@transaction.atomic
def confirm_booking(*, booking: Booking) -> Booking:
    """
    Confirm the booking if it contains at least one ticket and all tickets are still available.
    """
    booking = Booking.objects.select_for_update().get(pk=booking.pk)
    if booking.is_confirmed:
        raise ValidationError("Booking is already confirmed.")
    tickets_qs = getattr(booking, "tickets", None)
    if not tickets_qs or not tickets_qs.exists():
        raise ValidationError("Cannot confirm empty booking.")
    for ticket in tickets_qs.select_related("performance").all():
        perf = Performance.objects.select_for_update().get(pk=ticket.performance.pk)
        conflict = Ticket.objects.filter(
            performance=perf, row=ticket.row, seat=ticket.seat
        ).exclude(pk=ticket.pk).exists()
        if conflict:
            raise ValidationError(f"Seat {ticket.row}-{ticket.seat} for performance {perf.pk} is no longer available.")
    booking.is_confirmed = True
    booking.save(update_fields=("is_confirmed",))
    logger.info("Confirmed booking %s", booking.pk)
    return booking

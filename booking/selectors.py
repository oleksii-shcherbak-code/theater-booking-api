"""
Selectors for booking domain.

Read-only queries for bookings and tickets.
"""

from django.db.models import QuerySet

from booking.models import Booking


def booking_list_for_user(user) -> QuerySet[Booking]:
    """
    Return bookings for a specific user.

    Args:
        user: User instance.

    Returns:
        QuerySet of Booking objects.
    """
    return (
        Booking.objects
        .filter(user=user)
        .prefetch_related("tickets__performance")
        .order_by("-created_at")
    )

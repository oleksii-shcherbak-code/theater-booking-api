"""
Models for booking domain.

Contains booking and ticket entities.
"""

from django.conf import settings
from django.db import models


class Booking(models.Model):
    """
    Booking (cart/order) model.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Booking #{self.id} for {self.user}"


class Ticket(models.Model):
    """
    Ticket model representing a seat for a performance.
    """

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    performance = models.ForeignKey(
        "schedule.Performance",
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("performance", "row", "seat"),
                name="unique_ticket_per_seat",
            )
        ]

    def __str__(self) -> str:
        return f"{self.performance} row {self.row} seat {self.seat}"

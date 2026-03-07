from django.conf import settings
from django.db import models


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.pk}"


class Ticket(models.Model):
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
                name="unique_seat_per_performance",
            )
        ]

    def __str__(self):
        return f"{self.performance} row {self.row} seat {self.seat}"

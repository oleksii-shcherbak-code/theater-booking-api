from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Booking(models.Model):
    """
    Booking model representing a user's booking cart.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Booking #{self.pk}"


class Ticket(models.Model):
    """
    Ticket model representing a reserved seat for a performance.
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
    row = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seat = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("performance", "row", "seat"),
                name="unique_seat_per_performance",
            )
        ]

    def __str__(self) -> str:
        return f"{self.performance} row {self.row} seat {self.seat}"

    def clean(self) -> None:
        """
        Validate that row and seat are within the theatre hall bounds for the performance.
        """
        super().clean()
        performance_obj = getattr(self, "performance", None)
        if performance_obj is None:
            return
        theatre_hall = getattr(performance_obj, "theatre_hall", None)
        if theatre_hall is None:
            return
        if self.row is not None and self.row > theatre_hall.rows:
            raise ValidationError({"row": "Row is out of theatre hall bounds."})
        if self.seat is not None and self.seat > theatre_hall.seats_per_row:
            raise ValidationError({"seat": "Seat is out of theatre hall bounds."})
        starts_at = getattr(performance_obj, "starts_at", None)
        if starts_at is not None and starts_at < timezone.now():
            raise ValidationError({"performance": "Cannot create ticket for past performance."})

    def save(self, *args, **kwargs):
        """
        Run full_clean before saving to ensure model-level validation is enforced.
        """
        self.full_clean()
        return super().save(*args, **kwargs)

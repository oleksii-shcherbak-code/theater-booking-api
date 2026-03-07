from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        "plays.Play",
        on_delete=models.CASCADE,
        related_name="performances",
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    starts_at = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("theatre_hall", "starts_at"),
                name="unique_performance_per_hall_and_time",
            )
        ]

    def __str__(self) -> str:
        return f"{self.play.title} @ {self.starts_at}"

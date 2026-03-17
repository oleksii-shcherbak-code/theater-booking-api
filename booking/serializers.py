from typing import Any, Dict, Optional

from django.utils import timezone
from rest_framework import serializers

from booking.models import Booking, Ticket
from schedule.models import Performance


class TicketSerializer(serializers.ModelSerializer):
    """
    Use 'performance' field name because PrimaryKeyRelatedField returns an object.
    """
    performance = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all(),
    )

    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat")

    def validate_row(self, value: int) -> int:  # noqa
        if value < 1:
            raise serializers.ValidationError("Row must be greater than 0.")
        return value

    def validate_seat(self, value: int) -> int:  # noqa
        if value < 1:
            raise serializers.ValidationError("Seat must be greater than 0.")
        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        performance: Optional[Performance] = attrs.get("performance") or getattr(self.instance, "performance", None)
        if performance:
            starts_at = getattr(performance, "starts_at", None)
            if starts_at and starts_at < timezone.now():
                raise serializers.ValidationError("Cannot create ticket for past performance.")
            theatre_hall = getattr(performance, "theatre_hall", None)
            if theatre_hall:
                row = attrs.get("row") or getattr(self.instance, "row", None)
                seat = attrs.get("seat") or getattr(self.instance, "seat", None)
                if row and row > theatre_hall.rows:
                    raise serializers.ValidationError({"row": "Row is out of theatre hall bounds."})
                if seat and seat > theatre_hall.seats_per_row:
                    raise serializers.ValidationError({"seat": "Seat is out of theatre hall bounds."})
        return attrs


class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "user", "is_confirmed", "created_at", "tickets")
        read_only_fields = ("is_confirmed", "created_at")

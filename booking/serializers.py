"""
Serializers for booking domain.
"""

from rest_framework import serializers

from booking.models import Booking, Ticket
from booking.services import add_ticket_to_booking, confirm_booking
from schedule.models import Performance


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat")


class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "created_at", "is_confirmed", "tickets")


class AddTicketSerializer(serializers.Serializer):
    performance_id = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all(),
    )
    row = serializers.IntegerField(min_value=1)
    seat = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        booking = self.context["booking"]
        return add_ticket_to_booking(
            booking=booking,
            performance=validated_data["performance_id"],
            row=validated_data["row"],
            seat=validated_data["seat"],
        )


class ConfirmBookingSerializer(serializers.Serializer):
    def save(self, **kwargs):
        booking = self.context["booking"]
        return confirm_booking(booking=booking)

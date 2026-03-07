from rest_framework import serializers

from plays.models import Play
from schedule.models import Performance, TheatreHall
from schedule.services import create_performance


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_per_row")


class PerformanceListSerializer(serializers.ModelSerializer):
    play = serializers.StringRelatedField()
    theatre_hall = TheatreHallSerializer()

    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "starts_at",
            "ticket_price",
        )


class PerformanceCreateSerializer(serializers.Serializer):
    play_id = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(),
    )
    theatre_hall_id = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all(),
    )
    starts_at = serializers.DateTimeField()
    ticket_price = serializers.DecimalField(max_digits=8, decimal_places=2)

    def create(self, validated_data):
        return create_performance(
            play=validated_data["play_id"],
            theatre_hall=validated_data["theatre_hall_id"],
            starts_at=validated_data["starts_at"],
            ticket_price=validated_data["ticket_price"],
        )

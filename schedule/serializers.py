from datetime import datetime
from rest_framework import serializers
from schedule.models import Performance, TheatreHall
from plays.models import Play
from django.utils import timezone


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_per_row")


class PerformanceListSerializer(serializers.ModelSerializer):
    theatre_hall = TheatreHallSerializer()
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "starts_at", "ticket_price")


class PerformanceCreateSerializer(serializers.ModelSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "starts_at", "ticket_price")

    def validate_starts_at(self, value: datetime) -> datetime:  # noqa
        if value < timezone.now():
            raise serializers.ValidationError("starts_at cannot be in the past.")
        return value

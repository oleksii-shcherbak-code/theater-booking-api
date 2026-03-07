"""
API views for booking domain.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.models import Booking
from booking.selectors import booking_list_for_user
from booking.serializers import (
    AddTicketSerializer,
    BookingSerializer,
    ConfirmBookingSerializer,
)
from booking.services import create_booking


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    """

    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Return bookings for current user.
        """
        return booking_list_for_user(self.request.user)

    def perform_create(self, serializer):
        """
        Create booking for current user.
        """
        serializer.instance = create_booking(user=self.request.user)

    @action(detail=True, methods=["post"])
    def add_ticket(self, request, pk=None):
        """
        Add ticket to booking.
        """
        booking = self.get_object()
        serializer = AddTicketSerializer(
            data=request.data,
            context={"booking": booking},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        """
        Confirm booking.
        """
        booking = self.get_object()
        serializer = ConfirmBookingSerializer(
            context={"booking": booking},
        )
        serializer.save()
        return Response(status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from booking.serializers import BookingSerializer
from booking.services import create_booking
from booking.models import Booking


class BookingViewSet(viewsets.ModelViewSet):
    """
    Booking endpoints. Create follows DRF standard: create(self, request, *args, **kwargs)
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        booking = create_booking(user=request.user)
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

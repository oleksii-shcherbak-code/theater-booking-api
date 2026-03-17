from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer, TicketSerializer
from booking.services import add_ticket_to_booking, confirm_booking, create_booking
from schedule.models import Performance


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return bookings visible to the current user.
        Order queryset to avoid UnorderedObjectListWarning during pagination.
        """
        user = self.request.user
        if user.is_staff:
            qs = Booking.objects.all()
        else:
            qs = Booking.objects.filter(user=user)
        return qs.order_by("id")

    def create(self, request: Request, *args, **kwargs):
        booking = create_booking(user=request.user)
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="add_ticket")
    def add_ticket(self, request: Request, pk=None):
        booking = self.get_object()
        data = request.data
        perf_id = data.get("performance") or data.get("performance_id")
        if not perf_id:
            return Response({"detail": "performance id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            performance = Performance.objects.get(pk=perf_id)
        except Performance.DoesNotExist:
            return Response({"detail": "Invalid performance id."}, status=status.HTTP_400_BAD_REQUEST)
        TicketSerializer(data={"performance": performance.pk, "row": data.get("row"), "seat": data.get("seat")}).is_valid(raise_exception=True)
        try:
            add_ticket_to_booking(
                booking=booking,
                performance=performance,
                row=int(data.get("row", 0)),
                seat=int(data.get("seat", 0)),
            )
        except ValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request: Request, pk=None):
        booking = self.get_object()
        try:
            confirm_booking(booking=booking)
        except ValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

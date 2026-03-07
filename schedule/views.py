"""
API views for schedule domain.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from schedule.models import Performance
from schedule.selectors import performance_list
from schedule.serializers import (
    PerformanceCreateSerializer,
    PerformanceListSerializer,
)


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing performances.
    """

    queryset = Performance.objects.none()

    def get_queryset(self):
        """
        Return queryset for current action.
        """
        return performance_list()

    def get_serializer_class(self):
        """
        Select serializer based on action.
        """
        if self.action in ("list", "retrieve"):
            return PerformanceListSerializer
        return PerformanceCreateSerializer

    def get_permissions(self):
        """
        Allow read-only access for everyone,
        write access only for admin users.
        """
        if self.action in ("list", "retrieve"):
            return []
        return [IsAdminUser()]

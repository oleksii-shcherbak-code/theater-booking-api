from rest_framework import viewsets

from schedule.models import Performance
from schedule.selectors import performance_list
from schedule.serializers import (
    PerformanceCreateSerializer,
    PerformanceListSerializer,
)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.none()

    def get_queryset(self):
        return performance_list()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PerformanceListSerializer
        return PerformanceCreateSerializer

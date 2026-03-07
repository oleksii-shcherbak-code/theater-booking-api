from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from plays.models import Play
from plays.selectors import play_list
from plays.serializers import (
    PlayCreateUpdateSerializer,
    PlayDetailSerializer,
    PlayListSerializer,
)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.none()

    def get_queryset(self):
        return play_list()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlayCreateUpdateSerializer

    def get_permissions(self):
        """
        Allow read-only access for everyone,
        write access only for admin users.
        """
        if self.action in ["list", "retrieve"]:
            return []
        return [IsAdminUser()]

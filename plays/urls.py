from django.urls import include, path
from rest_framework.routers import DefaultRouter

from plays.views import PlayViewSet
from schedule.views import PerformanceViewSet

router = DefaultRouter()
router.register("plays", PlayViewSet, basename="plays")
router.register("performances", PerformanceViewSet, basename="performances")

urlpatterns = [
    path("", include(router.urls)),
]

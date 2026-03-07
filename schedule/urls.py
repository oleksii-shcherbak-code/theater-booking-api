from rest_framework.routers import DefaultRouter

from schedule.views import PerformanceViewSet

router = DefaultRouter()
router.register("performances", PerformanceViewSet, basename="performance")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from plays.views import PlayViewSet

router = DefaultRouter()
router.register("plays", PlayViewSet, basename="play")

urlpatterns = router.urls

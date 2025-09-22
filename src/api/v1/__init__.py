from rest_framework.routers import DefaultRouter

from .launch import LaunchViewSet
from .stats import LaunchStatsViewSet

router = DefaultRouter()

router.register(r"launches", LaunchViewSet, basename="launch")
router.register(r"stats", LaunchStatsViewSet, basename="launch-stats")

urlpatterns = router.urls

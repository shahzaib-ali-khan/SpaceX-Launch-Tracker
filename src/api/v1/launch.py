from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from tracker.models import Launch

from .serializers import LaunchSerializer


@method_decorator(cache_page(86400), name="dispatch")
class LaunchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Launch.objects.all().select_related("rocket", "launchpad")
    serializer_class = LaunchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "launch_datetime": ["gte", "lte"],
        "rocket__name": ["exact"],
        "success": ["exact"],
        "launchpad__name": ["exact"],
    }

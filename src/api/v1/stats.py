from typing import Any

from django.db.models import Case, Count, F, FloatField, Q, Value, When
from django.db.models.functions import TruncMonth, TruncYear
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from tracker.models import Launch


@method_decorator(cache_page(86400), name="dispatch")
class LaunchStatsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Launch.objects.all().select_related("rocket", "launchpad")

    def list(self, request, *args, **kwargs):
        qs = super().get_queryset()

        # Success rates by rocket
        rocket_stats = (
            qs.values("rocket__name")
            .annotate(
                total=Count("id"),
                success_count=Count("id", filter=Q(success=True)),
            )
            .annotate(
                success_rate=Case(
                    When(total=0, then=Value(0.0)),
                    default=(F("success_count") * 100.0 / F("total")),
                    output_field=FloatField(),
                )
            )
            .order_by("-total")
        )

        # Launches per site
        site_stats = (
            qs.values("launchpad__name").annotate(total=Count("id")).order_by("-total")
        )

        # Yearly frequency
        yearly_stats = (
            qs.annotate(year=TruncYear("launch_datetime"))
            .values("year")
            .annotate(count=Count("id"))
            .order_by("year")
        )

        # Monthly frequency
        monthly_stats = (
            qs.annotate(month=TruncMonth("launch_datetime"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        return Response(
            {
                "rocket_success_rates": list(rocket_stats),
                "launches_per_site": list(site_stats),
                "yearly_frequency": list(yearly_stats),
                "monthly_frequency": list(monthly_stats),
            },
            status=status.HTTP_200_OK,
        )

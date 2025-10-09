from django_filters import rest_framework as filters
from django_filters.fields import IsoDateTimeField

from tracker.models import Launch


class CustomDateFilter(filters.DateFilter):
    field_class = IsoDateTimeField

    def __init__(self, *args, **kwargs):
        # Accept multiple input formats. Supports both m-d-Y and ISO
        kwargs.setdefault(
            "input_formats",
            ["%d-%m-%Y"],
        )
        super().__init__(*args, **kwargs)


class LaunchFilter(filters.FilterSet):
    launch_date__gte = CustomDateFilter(method="filter_by_launch_date_gte")
    launch_date__lte = CustomDateFilter(method="filter_by_launch_date_lte")

    def filter_by_launch_date_gte(self, queryset, name, value):
        return queryset.filter(launch_datetime__date__gte=value)

    def filter_by_launch_date_lte(self, queryset, name, value):
        return queryset.filter(launch_datetime__date__lte=value)

    class Meta:
        model = Launch
        fields = {
            "rocket__name": ["exact"],
            "success": ["exact"],
            "launchpad__name": ["exact"],
            "launch_datetime": ["gte", "lte"],
        }

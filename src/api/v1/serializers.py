from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers

from tracker.models import Launch, Launchpad, Rocket


class RocketSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Rocket
        fields = (
            "id",
            "name",
            "mass",
            "active",
            "stages",
            "boosters",
            "success_rate_pct",
            "cost_per_launch",
            "first_flight",
            "type",
            "description",
        )
        read_only_fields = fields


class LaunchpadSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Launchpad
        fields = (
            "id",
            "name",
            "full_name",
            "locality",
            "region",
            "latitude",
            "longitude",
            "launch_attempts",
            "launch_successes",
            "status",
            "details",
        )
        read_only_fields = fields


class LaunchSerializer(serializers.ModelSerializer):
    rocket = RocketSerializer()
    launchpad = LaunchpadSerializer()

    class Meta:
        model = Launch
        fields = ("id", "name", "launch_datetime", "success", "rocket", "launchpad")
        read_only_fields = fields

from django.db import models
from enumfields import EnumField

from ..enums import LaunchpadStatus


class Launchpad(models.Model):
    # id from SpaceX API
    id = models.CharField(primary_key=True, max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    name = models.CharField(max_length=255, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    locality = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    latitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=False, blank=False
    )
    longitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=False, blank=False
    )

    launch_attempts = models.IntegerField(default=0, null=False, blank=False)
    launch_successes = models.IntegerField(default=0, null=False, blank=False)

    status = EnumField(LaunchpadStatus, max_length=55, default=LaunchpadStatus.ACTIVE)

    details = models.TextField(default="", null=True, blank=True)

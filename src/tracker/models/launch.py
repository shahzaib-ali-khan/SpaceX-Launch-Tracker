from django.db import models

from .launchpad import Launchpad
from .rocket import Rocket


class Launch(models.Model):
    # id from SpaceX API
    id = models.CharField(primary_key=True, max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)

    # date_utc in SpaceX API
    launch_datetime = models.DateTimeField()

    upcoming = models.BooleanField(null=False, blank=False)
    success = models.BooleanField(default=None, null=True, blank=True)

    rocket = models.ForeignKey(
        Rocket, on_delete=models.CASCADE, related_name="launches"
    )
    launchpad = models.ForeignKey(
        Launchpad, on_delete=models.CASCADE, related_name="launches"
    )

    details = models.TextField(default="", null=True, blank=True)

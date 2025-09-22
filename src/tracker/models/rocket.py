from django.db import models
from enumfields import EnumField

from ..enums import RocketType


class Rocket(models.Model):
    # id from SpaceX API
    id = models.CharField(primary_key=True, max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    name = models.CharField(max_length=255, null=False, blank=False)
    # in kg
    mass = models.PositiveIntegerField(null=False, blank=False)

    active = models.BooleanField(default=False)

    stages = models.IntegerField(null=False, blank=False)
    boosters = models.IntegerField(default=0, null=False, blank=False)
    success_rate_pct = models.IntegerField(default=0, null=False, blank=False)

    cost_per_launch = models.BigIntegerField(null=False, blank=False)

    first_flight = models.DateField(null=False, blank=False)

    type = EnumField(RocketType, max_length=50, null=False, blank=False)

    description = models.TextField(default="", null=True, blank=True)

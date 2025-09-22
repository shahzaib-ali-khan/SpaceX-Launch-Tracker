from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tracker.models import Launch, Rocket, Launchpad
from django.utils.timezone import now, timedelta


@pytest.fixture
def setup_launch_data():
    rocket1 = Rocket.objects.create(
        id="5e9d0d95eda69955f709d1eb",
        name="Falcon 9",
        mass=30146,
        type="rocket",
        active=True,
        stages=2,
        boosters=0,
        cost_per_launch=6700000,
        success_rate_pct=40,
        first_flight=datetime(2006, 3, 24).date(),
    )
    rocket2 = Rocket.objects.create(
        id="5t3d0d95eda69955f7124f",
        name="Starship",
        mass=20000,
        type="rocket",
        active=False,
        stages=2,
        boosters=2,
        cost_per_launch=5600000,
        success_rate_pct=20,
        first_flight=datetime(2004, 1, 24).date(),
    )
    site1 = Launchpad.objects.create(
        id="5e9e4501f5090910d4566f83",
        name="Cape Canaveral",
        full_name="Cape Canaveral",
        locality="Cape Canaveral",
        region="California",
        latitude=34.6440904,
        longitude=-120.5931438,
        launch_attempts=0,
        launch_successes=0,
    )
    site2 = Launchpad.objects.create(
        id="76gje4501f5090d4552314",
        name="Boca Chica",
        full_name="Boca Chica",
        locality="Boca Chica",
        region="Chica",
        latitude=23.6440904,
        longitude=-511.5931438,
        launch_attempts=0,
        launch_successes=0,
    )

    Launch.objects.create(
        id="5eb87cd9ffd86e000604b32a",
        rocket=rocket1,
        launchpad=site1,
        launch_datetime=now() - timedelta(days=400),
        success=True,
        upcoming=False,
    )
    Launch.objects.create(
        id="5eb87cdaffd86e000604b32b",
        rocket=rocket1,
        launchpad=site1,
        launch_datetime=now() - timedelta(days=200),
        success=False,
        upcoming=False,
    )
    Launch.objects.create(
        id="6876ecdaffdasfe0677671",
        rocket=rocket2,
        launchpad=site2,
        launch_datetime=now() - timedelta(days=30),
        success=True,
        upcoming=False,
    )


@pytest.mark.django_db
def test_stats_endpoint(api_client: APIClient, setup_launch_data: None):
    response = api_client.get(reverse("v1:launch-stats-list"))

    assert response.status_code == 200
    data = response.json()

    # Top-level keys
    assert "rocket_success_rates" in data
    assert "launches_per_site" in data
    assert "yearly_frequency" in data
    assert "monthly_frequency" in data

    # Rocket success rates
    falcon = next(
        item
        for item in data["rocket_success_rates"]
        if item["rocket__name"] == "Falcon 9"
    )
    assert falcon["total"] == 2
    assert 0 <= falcon["success_rate"] <= 100

    starship = next(
        item
        for item in data["rocket_success_rates"]
        if item["rocket__name"] == "Starship"
    )
    assert starship["success_rate"] == 100.0

    # Launches per site
    assert any(
        site["launchpad__name"] == "Cape Canaveral"
        for site in data["launches_per_site"]
    )
    assert any(
        site["launchpad__name"] == "Boca Chica" for site in data["launches_per_site"]
    )

    # Frequencies should be non-empty
    assert len(data["yearly_frequency"]) > 0
    assert len(data["monthly_frequency"]) > 0

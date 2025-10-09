from datetime import datetime, timezone, timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tracker.models import Launch


@pytest.mark.django_db
def test_list_launches(api_client: APIClient, launch1: Launch, launch2: Launch):
    response = api_client.get(reverse("v1:launch-list"))

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


@pytest.mark.django_db
def test_list_launches_ensure_cache_working(
    api_client: APIClient, launch1: Launch, launch2: Launch
):
    response = api_client.get(reverse("v1:launch-list"))

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
    assert "Cache-Control" in response.headers
    assert response.headers["Cache-Control"] == "max-age=86400"


@pytest.mark.django_db
def test_retrieve_launch(api_client, launch1: Launch):
    response = api_client.get(reverse("v1:launch-detail", args=[launch1.id]))

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == launch1.name


@pytest.mark.django_db
def test_filter_launch_datetime_gte(api_client, launch1: Launch, launch2: Launch):
    response = api_client.get(
        reverse("v1:launch-list"),
        {"launch_datetime__gte": launch2.launch_datetime.isoformat()},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == launch2.id


@pytest.mark.django_db
def test_filter_launch_datetime_lte(api_client, launch1: Launch, launch2: Launch):
    response = api_client.get(
        reverse("v1:launch-list"),
        {"launch_datetime__lte": launch1.launch_datetime.isoformat()},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == launch1.id


@pytest.mark.django_db
def test_filter_by_rocket_name(api_client, launch1: Launch, launch2: Launch):
    response = api_client.get(
        reverse("v1:launch-list"), {"rocket__name": launch2.rocket.name}
    )

    assert response.status_code == 200
    data = response.json()
    launches = data["results"]

    assert all(item["rocket"]["id"] == str(launch2.rocket.id) for item in launches)


@pytest.mark.django_db
def test_filter_by_success(api_client, launch1: Launch, launch2: Launch):
    response = api_client.get(reverse("v1:launch-list"), {"success": "true"})

    assert response.status_code == 200
    data = response.json()
    launches = data["results"]

    assert len(data["results"]) == 1
    assert launches[0]["id"] == launch2.id


@pytest.mark.django_db
def test_filter_by_launchpad_name(api_client, launch1: Launch, launch2: Launch):
    response = api_client.get(
        reverse("v1:launch-list"), {"launchpad__name": launch1.launchpad.name}
    )

    assert response.status_code == 200
    data = response.json()
    launches = data["results"]

    assert len(data["results"]) == 1
    assert launches[0]["launchpad"]["id"] == str(launch1.launchpad.id)


@pytest.mark.django_db
@pytest.mark.parametrize("dates_in_two_foramts", ["2025-10-06", "06-10-2025"])
def test_filter_launch_date_gte(
    api_client, launch1: Launch, launch2: Launch, dates_in_two_foramts: str
):
    response = api_client.get(
        reverse("v1:launch-list"),
        {"launch_date__gte": dates_in_two_foramts},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == launch2.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "dates_in_two_formats",
    [
        (datetime.now(tz=timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d"),
        (datetime.now(tz=timezone.utc) - timedelta(days=3)).strftime("%d-%m-%Y"),
    ],
)
def test_filter_launch_date_gte(
    api_client, launch1: Launch, launch2: Launch, dates_in_two_formats: str
):
    response = api_client.get(
        reverse("v1:launch-list"),
        {"launch_date__gte": dates_in_two_formats},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == launch2.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "dates_in_two_formats",
    [
        (datetime.now(tz=timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%d"),
        (datetime.now(tz=timezone.utc) - timedelta(days=10)).strftime("%d-%m-%Y"),
    ],
)
def test_filter_launch_date_lte(
    api_client, launch1: Launch, launch2: Launch, dates_in_two_formats: str
):
    response = api_client.get(
        reverse("v1:launch-list"),
        {"launch_date__lte": dates_in_two_formats},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == launch1.id

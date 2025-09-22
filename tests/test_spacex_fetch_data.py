import pytest
from django.core.management import call_command

from tracker.models import Launch, Launchpad, Rocket

# At the time when the test was written there were 4 rockets, 6 launchpads and 205 launches


@pytest.mark.django_db
def test_fetch_spacex_data_creates_new_objects(
    mock_spacex_api_endpoint_launches: None,
    mock_spacex_api_endpoint_launchpads: None,
    mock_spacex_api_endpoint_rockets: None,
):
    call_command("fetch_spacex_data")

    assert Rocket.objects.count() == 2
    assert Launchpad.objects.count() == 2
    assert Launch.objects.count() == 2


@pytest.mark.django_db
def test_fetch_spacex_data_again_donot_create_existing_objects(
    mock_spacex_api_endpoint_launches: None,
    mock_spacex_api_endpoint_launchpads: None,
    mock_spacex_api_endpoint_rockets: None,
):
    call_command("fetch_spacex_data")

    assert Rocket.objects.count() == 2
    assert Launchpad.objects.count() == 2
    assert Launch.objects.count() == 2

    # Calling command again will not create same objects again
    call_command("fetch_spacex_data")

    assert Rocket.objects.count() == 2
    assert Launchpad.objects.count() == 2
    assert Launch.objects.count() == 2


@pytest.mark.django_db
def test_fetch_spacex_data_skips_existing_rocket(
    mock_spacex_api_endpoint_launches: None,
    mock_spacex_api_endpoint_launchpads: None,
    mock_spacex_api_endpoint_rockets: None,
    falcon_1_rocket: Rocket,
):
    # Ensure before running command there was a rocket in the database
    assert Rocket.objects.count() == 1

    call_command("fetch_spacex_data")

    assert Rocket.objects.count() == 2
    assert Launchpad.objects.count() == 2
    assert Launch.objects.count() == 2

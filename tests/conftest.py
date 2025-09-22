from datetime import datetime, timedelta, timezone

import pytest
from rest_framework.test import APIClient

from tracker.enums import LaunchpadStatus
from tracker.models import Launch, Launchpad, Rocket


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def falcon_1_rocket() -> Rocket:
    return Rocket.objects.create(
        id="5e9d0d95eda69955f709d1eb",
        name="Falcon 1",
        mass=30146,
        type="rocket",
        active=False,
        stages=2,
        boosters=0,
        cost_per_launch=6700000,
        success_rate_pct=40,
        first_flight=datetime(2006, 3, 24).date(),
    )


@pytest.fixture
def launch1(falcon_1_rocket: Rocket) -> Launch:
    lp1 = Launchpad.objects.create(
        id="lp1",
        name="CCAFS SLC 40",
        full_name="Cape Canaveral Air Force Station Space Launch Complex 40",
        locality="Cape Canaveral",
        region="Florida",
        launch_attempts=10,
        launch_successes=8,
        latitude=52.6440904,
        longitude=-120.5931438,
        status=LaunchpadStatus.ACTIVE,
    )

    return Launch.objects.create(
        id="l1",
        name="FalconSat",
        launch_datetime=datetime.now(tz=timezone.utc) - timedelta(days=10),
        success=False,
        rocket=falcon_1_rocket,
        launchpad=lp1,
        upcoming=False,
        details="Engine failure at 33 seconds",
    )


@pytest.fixture
def launch2(falcon_1_rocket: Rocket) -> Launch:
    lp2 = Launchpad.objects.create(
        id="lp2",
        name="KSC LC 39A",
        full_name="Kennedy Space Center Launch Complex 39A",
        locality="Merritt Island",
        region="Florida",
        launch_attempts=20,
        launch_successes=18,
        latitude=34.6440904,
        longitude=-120.5931438,
        status=LaunchpadStatus.ACTIVE,
    )

    return Launch.objects.create(
        id="l2",
        name="CRS-20",
        launch_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
        success=True,
        rocket=falcon_1_rocket,
        launchpad=lp2,
        upcoming=False,
        details="Successful resupply mission",
    )


# Mock exact SpaceX API endpoints
@pytest.fixture
def mock_spacex_api_endpoint_rockets(requests_mock) -> None:
    requests_mock.get(
        "https://api.spacexdata.com/v4/rockets",
        json=[
            {
                "height": {"meters": 22.25, "feet": 73},
                "diameter": {"meters": 1.68, "feet": 5.5},
                "mass": {"kg": 30146, "lb": 66460},
                "first_stage": {
                    "thrust_sea_level": {"kN": 420, "lbf": 94000},
                    "thrust_vacuum": {"kN": 480, "lbf": 110000},
                    "reusable": False,
                    "engines": 1,
                    "fuel_amount_tons": 44.3,
                    "burn_time_sec": 169,
                },
                "second_stage": {
                    "thrust": {"kN": 31, "lbf": 7000},
                    "payloads": {
                        "composite_fairing": {
                            "height": {"meters": 3.5, "feet": 11.5},
                            "diameter": {"meters": 1.5, "feet": 4.9},
                        },
                        "option_1": "composite fairing",
                    },
                    "reusable": False,
                    "engines": 1,
                    "fuel_amount_tons": 3.38,
                    "burn_time_sec": 378,
                },
                "engines": {
                    "isp": {"sea_level": 267, "vacuum": 304},
                    "thrust_sea_level": {"kN": 420, "lbf": 94000},
                    "thrust_vacuum": {"kN": 480, "lbf": 110000},
                    "number": 1,
                    "type": "merlin",
                    "version": "1C",
                    "layout": "single",
                    "engine_loss_max": 0,
                    "propellant_1": "liquid oxygen",
                    "propellant_2": "RP-1 kerosene",
                    "thrust_to_weight": 96,
                },
                "landing_legs": {"number": 0, "material": None},
                "payload_weights": [
                    {"id": "leo", "name": "Low Earth Orbit", "kg": 450, "lb": 992}
                ],
                "flickr_images": [
                    "https://imgur.com/DaCfMsj.jpg",
                    "https://imgur.com/azYafd8.jpg",
                ],
                "name": "Falcon 1",
                "type": "rocket",
                "active": False,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 6700000,
                "success_rate_pct": 40,
                "first_flight": "2006-03-24",
                "country": "Republic of the Marshall Islands",
                "company": "SpaceX",
                "wikipedia": "https://en.wikipedia.org/wiki/Falcon_1",
                "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX during 2006-2009. On 28 September 2008, Falcon 1 became the first privately-developed liquid-fuel launch vehicle to go into orbit around the Earth.",
                "id": "5e9d0d95eda69955f709d1eb",
            },
            {
                "height": {"meters": 70, "feet": 229.6},
                "diameter": {"meters": 3.7, "feet": 12},
                "mass": {"kg": 549054, "lb": 1207920},
                "first_stage": {
                    "thrust_sea_level": {"kN": 7607, "lbf": 1710000},
                    "thrust_vacuum": {"kN": 8227, "lbf": 1849500},
                    "reusable": True,
                    "engines": 9,
                    "fuel_amount_tons": 385,
                    "burn_time_sec": 162,
                },
                "second_stage": {
                    "thrust": {"kN": 934, "lbf": 210000},
                    "payloads": {
                        "composite_fairing": {
                            "height": {"meters": 13.1, "feet": 43},
                            "diameter": {"meters": 5.2, "feet": 17.1},
                        },
                        "option_1": "dragon",
                    },
                    "reusable": False,
                    "engines": 1,
                    "fuel_amount_tons": 90,
                    "burn_time_sec": 397,
                },
                "engines": {
                    "isp": {"sea_level": 288, "vacuum": 312},
                    "thrust_sea_level": {"kN": 845, "lbf": 190000},
                    "thrust_vacuum": {"kN": 914, "lbf": 205500},
                    "number": 9,
                    "type": "merlin",
                    "version": "1D+",
                    "layout": "octaweb",
                    "engine_loss_max": 2,
                    "propellant_1": "liquid oxygen",
                    "propellant_2": "RP-1 kerosene",
                    "thrust_to_weight": 180.1,
                },
                "landing_legs": {"number": 4, "material": "carbon fiber"},
                "payload_weights": [
                    {"id": "leo", "name": "Low Earth Orbit", "kg": 22800, "lb": 50265},
                    {
                        "id": "gto",
                        "name": "Geosynchronous Transfer Orbit",
                        "kg": 8300,
                        "lb": 18300,
                    },
                    {"id": "mars", "name": "Mars Orbit", "kg": 4020, "lb": 8860},
                ],
                "flickr_images": [
                    "https://farm1.staticflickr.com/929/28787338307_3453a11a77_b.jpg",
                    "https://farm4.staticflickr.com/3955/32915197674_eee74d81bb_b.jpg",
                    "https://farm1.staticflickr.com/293/32312415025_6841e30bf1_b.jpg",
                    "https://farm1.staticflickr.com/623/23660653516_5b6cb301d1_b.jpg",
                    "https://farm6.staticflickr.com/5518/31579784413_d853331601_b.jpg",
                    "https://farm1.staticflickr.com/745/32394687645_a9c54a34ef_b.jpg",
                ],
                "name": "Falcon 9",
                "type": "rocket",
                "active": True,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 50000000,
                "success_rate_pct": 98,
                "first_flight": "2010-06-04",
                "country": "United States",
                "company": "SpaceX",
                "wikipedia": "https://en.wikipedia.org/wiki/Falcon_9",
                "description": "Falcon 9 is a two-stage rocket designed and manufactured by SpaceX for the reliable and safe transport of satellites and the Dragon spacecraft into orbit.",
                "id": "5e9d0d95eda69973a809d1ec",
            },
        ],
    )


@pytest.fixture
def mock_spacex_api_endpoint_launchpads(requests_mock) -> None:
    requests_mock.get(
        "https://api.spacexdata.com/v4/launchpads",
        json=[
            {
                "images": {"large": ["https://i.imgur.com/7uXe1Kv.png"]},
                "name": "VAFB SLC 3W",
                "full_name": "Vandenberg Space Force Base Space Launch Complex 3W",
                "locality": "Vandenberg Space Force Base",
                "region": "California",
                "latitude": 34.6440904,
                "longitude": -120.5931438,
                "launch_attempts": 0,
                "launch_successes": 0,
                "rockets": ["5e9d0d95eda69955f709d1eb"],
                "timezone": "America/Los_Angeles",
                "launches": ["5eb87cd9ffd86e000604b32a"],
                "status": "retired",
                "details": "SpaceX's original west coast launch pad for Falcon 1. It was used in a static fire test but was never employed for a launch, and was abandoned due to range scheduling conflicts arising from overflying other active pads.",
                "id": "5e9e4501f5090910d4566f83",
            },
            {
                "images": {"large": ["https://i.imgur.com/9oEMXwa.png"]},
                "name": "CCSFS SLC 40",
                "full_name": "Cape Canaveral Space Force Station Space Launch Complex 40",
                "locality": "Cape Canaveral",
                "region": "Florida",
                "latitude": 28.5618571,
                "longitude": -80.577366,
                "launch_attempts": 99,
                "launch_successes": 97,
                "rockets": ["5e9d0d95eda69955f709d1eb"],
                "timezone": "America/New_York",
                "launches": ["5eb87cdaffd86e000604b32b"],
                "status": "active",
                "details": "SpaceX's primary Falcon 9 pad, where all east coast Falcon 9s launched prior to the AMOS-6 anomaly. Previously used alongside SLC-41 to launch Titan rockets for the US Air Force, the pad was heavily damaged by the AMOS-6 anomaly in September 2016. It returned to flight with CRS-13 on December 15, 2017, boasting an upgraded throwback-style Transporter-Erector modeled after that at LC-39A.",
                "id": "5e9e4501f509094ba4566f84",
            },
        ],
    )


@pytest.fixture
def mock_spacex_api_endpoint_launches(requests_mock) -> None:
    requests_mock.get(
        "https://api.spacexdata.com/v4/launches",
        json=[
            {
                "fairings": {
                    "reused": False,
                    "recovery_attempt": False,
                    "recovered": False,
                    "ships": [],
                },
                "links": {
                    "patch": {
                        "small": "https://images2.imgbox.com/94/f2/NN6Ph45r_o.png",
                        "large": "https://images2.imgbox.com/5b/02/QcxHUb5V_o.png",
                    },
                    "reddit": {
                        "campaign": None,
                        "launch": None,
                        "media": None,
                        "recovery": None,
                    },
                    "flickr": {"small": [], "original": []},
                    "presskit": None,
                    "webcast": "https://www.youtube.com/watch?v=0a_00nJ_Y88",
                    "youtube_id": "0a_00nJ_Y88",
                    "article": "https://www.space.com/2196-spacex-inaugural-falcon-1-rocket-lost-launch.html",
                    "wikipedia": "https://en.wikipedia.org/wiki/DemoSat",
                },
                "static_fire_date_utc": "2006-03-17T00:00:00.000Z",
                "static_fire_date_unix": 1142553600,
                "net": False,
                "window": 0,
                "rocket": "5e9d0d95eda69955f709d1eb",
                "success": False,
                "failures": [
                    {"time": 33, "altitude": None, "reason": "merlin engine failure"}
                ],
                "details": "Engine failure at 33 seconds and loss of vehicle",
                "crew": [],
                "ships": [],
                "capsules": [],
                "payloads": ["5eb0e4b5b6c3bb0006eeb1e1"],
                "launchpad": "5e9e4501f5090910d4566f83",
                "flight_number": 1,
                "name": "FalconSat",
                "date_utc": "2006-03-24T22:30:00.000Z",
                "date_unix": 1143239400,
                "date_local": "2006-03-25T10:30:00+12:00",
                "date_precision": "hour",
                "upcoming": False,
                "cores": [
                    {
                        "core": "5e9e289df35918033d3b2623",
                        "flight": 1,
                        "gridfins": False,
                        "legs": False,
                        "reused": False,
                        "landing_attempt": False,
                        "landing_success": None,
                        "landing_type": None,
                        "landpad": None,
                    }
                ],
                "auto_update": True,
                "tbd": False,
                "launch_library_id": None,
                "id": "5eb87cd9ffd86e000604b32a",
            },
            {
                "fairings": {
                    "reused": False,
                    "recovery_attempt": False,
                    "recovered": False,
                    "ships": [],
                },
                "links": {
                    "patch": {
                        "small": "https://images2.imgbox.com/f9/4a/ZboXReNb_o.png",
                        "large": "https://images2.imgbox.com/80/a2/bkWotCIS_o.png",
                    },
                    "reddit": {
                        "campaign": None,
                        "launch": None,
                        "media": None,
                        "recovery": None,
                    },
                    "flickr": {"small": [], "original": []},
                    "presskit": None,
                    "webcast": "https://www.youtube.com/watch?v=Lk4zQ2wP-Nc",
                    "youtube_id": "Lk4zQ2wP-Nc",
                    "article": "https://www.space.com/3590-spacex-falcon-1-rocket-fails-reach-orbit.html",
                    "wikipedia": "https://en.wikipedia.org/wiki/DemoSat",
                },
                "static_fire_date_utc": None,
                "static_fire_date_unix": None,
                "net": False,
                "window": 0,
                "rocket": "5e9d0d95eda69955f709d1eb",
                "success": False,
                "failures": [
                    {
                        "time": 301,
                        "altitude": 289,
                        "reason": "harmonic oscillation leading to premature engine shutdown",
                    }
                ],
                "details": "Successful first stage burn and transition to second stage, maximum altitude 289 km, Premature engine shutdown at T+7 min 30 s, Failed to reach orbit, Failed to recover first stage",
                "crew": [],
                "ships": [],
                "capsules": [],
                "payloads": ["5eb0e4b6b6c3bb0006eeb1e2"],
                "launchpad": "5e9e4501f509094ba4566f84",
                "flight_number": 2,
                "name": "DemoSat",
                "date_utc": "2007-03-21T01:10:00.000Z",
                "date_unix": 1174439400,
                "date_local": "2007-03-21T13:10:00+12:00",
                "date_precision": "hour",
                "upcoming": False,
                "cores": [
                    {
                        "core": "5e9e289ef35918416a3b2624",
                        "flight": 1,
                        "gridfins": False,
                        "legs": False,
                        "reused": False,
                        "landing_attempt": False,
                        "landing_success": None,
                        "landing_type": None,
                        "landpad": None,
                    }
                ],
                "auto_update": True,
                "tbd": False,
                "launch_library_id": None,
                "id": "5eb87cdaffd86e000604b32b",
            },
        ],
    )

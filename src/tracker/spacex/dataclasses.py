import decimal
from dataclasses import dataclass
from typing import Optional


@dataclass
class RocketDTO:
    id: str
    name: str
    mass: int  # in kg
    active: bool
    stages: int
    boosters: int
    success_rate_pct: int
    cost_per_launch: int
    first_flight: str
    type: str
    description: Optional[str]


@dataclass
class LaunchpadDTO:
    id: str
    name: str
    full_name: str
    locality: str
    region: str
    launch_attempts: int
    launch_successes: int
    status: str
    latitude: decimal.Decimal
    longitude: decimal.Decimal
    details: Optional[str]


@dataclass
class LaunchDTO:
    id: str
    name: str
    date_utc: str
    upcoming: bool
    rocket: RocketDTO
    rocket: str
    launchpad: str
    details: Optional[str]
    success: bool | None = None

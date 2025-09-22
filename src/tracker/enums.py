from enum import Enum, member


class RocketType(Enum):
    MERLIN = "merlin"
    ROCKET = "rocket"
    RAPTOR = "raptor"

    @member
    class Labels:
        MERLIN = "Merlin"
        ROCKET = "Rocket"
        RAPTOR = "Raptor"


class LaunchpadStatus(Enum):
    ACTIVE = "active"
    RETIRED = "retired"
    UNDER_CONSTRUCTION = "under construction"

    @member
    class Labels:
        ACTIVE = "Active"
        RETIRED = "Retired"
        UNDER_CONSTRUCTION = "Under Construction"

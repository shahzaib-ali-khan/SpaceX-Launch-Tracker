from datetime import datetime

import structlog
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from ...models import Launch, Launchpad, Rocket
from ...spacex.client import SpaceX

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    help = "Fetches SpaceX data and stores it locally in the DB."

    def handle(self, *args, **options):
        spacex = SpaceX()
        data = spacex.fetch_data()

        with atomic():
            # Rockets
            existing_rockets = set(Rocket.objects.values_list("id", flat=True))
            new_rockets = [
                Rocket(
                    id=r.id,
                    name=r.name,
                    mass=r.mass,
                    type=r.type,
                    active=r.active,
                    stages=r.stages,
                    boosters=r.boosters,
                    cost_per_launch=r.cost_per_launch,
                    success_rate_pct=r.success_rate_pct,
                    first_flight=r.first_flight,
                    description=r.description,
                )
                for r in data["rockets"]
                if r.id not in existing_rockets
            ]
            Rocket.objects.bulk_create(new_rockets)

            logger.info(
                "Rockets synced",
                new=len(new_rockets),
                total=len(existing_rockets) + len(new_rockets),
            )

            # Launchpads
            existing_launchpads = set(Launchpad.objects.values_list("id", flat=True))
            new_launchpads = [
                Launchpad(
                    id=lp.id,
                    name=lp.name,
                    full_name=lp.full_name,
                    locality=lp.locality,
                    region=lp.region,
                    launch_attempts=lp.launch_attempts,
                    launch_successes=lp.launch_successes,
                    status=lp.status,
                    latitude=lp.latitude,
                    longitude=lp.longitude,
                    details=lp.details,
                )
                for lp in data["launchpads"]
                if lp.id not in existing_launchpads
            ]
            Launchpad.objects.bulk_create(new_launchpads)

            logger.info(
                "Launchpads synced",
                new=len(new_launchpads),
                total=len(existing_launchpads) + len(new_launchpads),
            )

            # Launches
            existing_launches = set(Launch.objects.values_list("id", flat=True))

            # Prefetch related rockets + launchpads into dicts
            rocket_map = {r.id: r for r in Rocket.objects.all()}
            launchpad_map = {lp.id: lp for lp in Launchpad.objects.all()}

            new_launches = []
            for l in data["launches"]:
                if l.id in existing_launches:
                    continue

                try:
                    rocket = rocket_map[l.rocket]
                    launchpad = launchpad_map[l.launchpad]
                except KeyError as e:
                    logger.warning(
                        f"Skipping launch {l.id}: missing related object {e}"
                    )
                    continue

                new_launches.append(
                    Launch(
                        id=l.id,
                        name=l.name,
                        launch_datetime=datetime.fromisoformat(
                            l.date_utc.replace("Z", "+00:00")
                        ),
                        upcoming=l.upcoming,
                        success=l.success,
                        rocket=rocket,
                        launchpad=launchpad,
                        details=l.details,
                    )
                )

            Launch.objects.bulk_create(new_launches)

            logger.info(
                "Launches synced",
                new=len(new_launches),
                total=len(existing_launches) + len(new_launches),
            )

            logger.info("SpaceX data fetch completed")

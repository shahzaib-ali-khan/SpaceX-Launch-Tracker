import time
from typing import List
from urllib.parse import urljoin

import requests
import structlog
from django.conf import settings
from requests import ConnectionError, RequestException, Response, Timeout

from .dataclasses import LaunchDTO, LaunchpadDTO, RocketDTO

logger = structlog.get_logger(__name__)


class ThirdPartyAPI:
    def __init__(
        self, max_retries: int = 3, base_backoff: int = 2, timeout: int = 10
    ) -> None:
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.timeout = timeout

    def api_call(
        self,
        url: str,
        method: str = "post",
        data: dict = None,
    ) -> Response:
        extra_args = {}
        if method == "post":
            extra_args = {"json": data}

        retries = 0
        while retries <= self.max_retries:
            try:
                response = getattr(requests, method)(
                    url,
                    **extra_args,
                )
                return response
            except RequestException as exc:
                wait_time = 2**retries
                logger.error(
                    f"Error fetching {url}: {exc}. Retry {retries + 1}/{self.max_retries} in {wait_time}s"
                )
                time.sleep(wait_time)
            except ValueError as exc:
                logger.error(f"Value error in {url}: {exc}")
                raise
            except (Timeout, ConnectionError) as exc:
                wait_time = self.base_backoff**retries
                logger.warning(
                    f"Transient error calling {url}: {exc}. Retry {retries + 1}/{self.max_retries} in {wait_time}s"
                )
                time.sleep(wait_time)

            retries += 1
            if retries >= self.max_retries:
                logger.error(f"Max retries reached for {url}. Failing permanently.")
                raise

        raise RuntimeError("api_call failed unexpectedly")

    def get_json_data(
        self,
        url: str,
        method: str = "post",
        data: dict = None,
    ) -> dict:
        return self.api_call(url, method, data).json()


class SpaceX(ThirdPartyAPI):
    BASE_URL = settings.SPACEX_BASE_URL

    def fetch_launches(self) -> List[LaunchDTO]:
        url = urljoin(self.BASE_URL, "launches")
        data = super().get_json_data(url, "get", None)

        return [
            LaunchDTO(
                id=item.get("id"),
                name=item.get("name"),
                date_utc=item.get("date_utc"),
                upcoming=item.get("upcoming"),
                success=item.get("success"),
                rocket=item.get("rocket"),
                launchpad=item.get("launchpad"),
                details=item.get("details"),
            )
            for item in data
        ]

    def fetch_rockets(self) -> List[RocketDTO]:
        url = urljoin(self.BASE_URL, "rockets")
        data = super().get_json_data(url, "get", None)

        return [
            RocketDTO(
                id=item.get("id"),
                name=item.get("name"),
                mass=item.get("mass", {}).get("kg"),
                type=item.get("type"),
                active=item.get("active"),
                stages=item.get("stages"),
                boosters=item.get("boosters"),
                cost_per_launch=item.get("cost_per_launch"),
                success_rate_pct=item.get("success_rate_pct"),
                first_flight=item.get("first_flight"),
                description=item.get("description", ""),
            )
            for item in data
        ]

    def fetch_launchpads(self) -> List[LaunchpadDTO]:
        url = urljoin(self.BASE_URL, "launchpads")
        data = super().get_json_data(url, "get", None)

        return [
            LaunchpadDTO(
                id=item.get("id"),
                name=item.get("name"),
                full_name=item.get("full_name"),
                locality=item.get("locality"),
                region=item.get("region"),
                launch_attempts=item.get("launch_attempts"),
                launch_successes=item.get("launch_successes"),
                status=item.get("status"),
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
                details=item.get("details", ""),
            )
            for item in data
        ]

    def fetch_data(self):
        return {
            "launches": self.fetch_launches(),
            "rockets": self.fetch_rockets(),
            "launchpads": self.fetch_launchpads(),
        }

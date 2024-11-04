from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, TypedDict, cast

import aiohttp
from aiohttp import ClientError
from aiohttp_prometheus_exporter.trace import PrometheusTraceConfig
from diskcache import Cache

from matrix_alertbot.errors import (
    AlertmanagerClientError,
    AlertmanagerServerError,
    AlertNotFoundError,
    SilenceExpiredError,
    SilenceExtendError,
    SilenceNotFoundError,
)

DEFAULT_DURATION = timedelta(hours=3)
MAX_DURATION = timedelta(days=3652)


logger = logging.getLogger(__name__)

AlertDict = TypedDict(
    "AlertDict",
    {
        "fingerprint": str,
        "labels": Dict[str, str],
    },
)

SilenceDict = TypedDict(
    "SilenceDict",
    {
        "id": str,
        "matchers": List[Dict[str, Any]],
        "createdBy": str,
        "status": Dict[str, str],
    },
)


class AlertmanagerClient:
    def __init__(self, url: str, cache: Cache) -> None:
        self.api_url = f"{url}/api/v2"
        self.cache = cache
        self.session = None

    async def start(self) -> None:
        self.session = aiohttp.ClientSession(trace_configs=[PrometheusTraceConfig()])

    async def close(self) -> None:
        if self.session is not None:
            await self.session.close()

    async def __aenter__(self) -> AlertmanagerClient:
        if self.session is None:
            await self.start()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def get_alerts(self) -> List[AlertDict]:
        if self.session is None:
            raise AlertmanagerClientError("Alertmanager client is not started")

        try:
            async with self.session.get(f"{self.api_url}/alerts") as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as e:
            raise AlertmanagerServerError(
                "Cannot fetch alerts from Alertmanager"
            ) from e

    async def get_alert(self, fingerprint: str) -> AlertDict:
        logger.debug(f"Fetching details for alert with fingerprint {fingerprint}")
        alerts = await self.get_alerts()
        return self._find_alert(fingerprint, alerts)

    async def get_silences(self) -> List[SilenceDict]:
        if self.session is None:
            raise AlertmanagerClientError("Alertmanager client is not started")

        try:
            async with self.session.get(f"{self.api_url}/silences") as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as e:
            raise AlertmanagerServerError(
                "Cannot fetch silences from Alertmanager"
            ) from e

    async def get_silence(self, silence_id: str) -> SilenceDict:
        logger.debug(f"Fetching details for silence with ID {silence_id}")
        silences = await self.get_silences()
        return self._find_silence(silence_id, silences)

    async def create_silence(
        self,
        fingerprint: str,
        user: str,
        duration_seconds: Optional[int] = None,
    ) -> str:
        alert = await self.get_alert(fingerprint)

        logger.debug(f"Creating silence for alert with fingerprint {fingerprint}")

        silence_matchers = [
            {"name": label, "value": value, "isRegex": False, "isEqual": True}
            for label, value in alert["labels"].items()
        ]

        return await self._create_or_update_silence(
            fingerprint, silence_matchers, user, duration_seconds
        )

    async def update_silence(
        self,
        fingerprint: str,
        user: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        *,
        force: bool = False,
    ) -> str:
        logger.debug(
            f"Reading silence for alert with fingerprint {fingerprint} from cache"
        )

        cache_result = cast(
            Optional[Tuple[str, int]], self.cache.get(fingerprint, expire_time=True)
        )
        if cache_result is not None:
            silence_id, expire_time = cache_result
        else:
            silence_id = None
            expire_time = None

        if silence_id is None:
            raise SilenceNotFoundError(
                f"Cannot find silence for alert with fingerprint {fingerprint} in cache."
            )

        logger.debug(
            f"Updating silence with ID {silence_id} for alert with fingerprint {fingerprint}"
        )

        # If silence in cache had a duration, and the new silence doesn't have a duration
        # then we cannot update this silence.
        if not force and duration_seconds is None and expire_time is not None:
            raise SilenceExtendError(
                f"Cannot extend silence ID {silence_id} with static duration."
            )

        silence = await self.get_silence(silence_id)
        if user is None:
            user = silence["createdBy"]
        silence_matchers = silence["matchers"]

        return await self._create_or_update_silence(
            fingerprint, silence_matchers, user, duration_seconds, silence_id
        )

    async def create_or_update_silence(
        self,
        fingerprint: str,
        user: str,
        duration_seconds: Optional[int] = None,
        *,
        force: bool = False,
    ) -> str:
        try:
            silence_id = await self.update_silence(
                fingerprint, user, duration_seconds, force=force
            )
        except SilenceNotFoundError:
            silence_id = await self.create_silence(fingerprint, user, duration_seconds)
        return silence_id

    async def _create_or_update_silence(
        self,
        fingerprint: str,
        silence_matchers: List,
        user: str,
        duration_seconds: Optional[int] = None,
        silence_id: Optional[str] = None,
    ) -> str:
        if self.session is None:
            raise AlertmanagerClientError("Alertmanager client is not started")

        if duration_seconds is None:
            duration_delta = DEFAULT_DURATION
        elif duration_seconds > MAX_DURATION.total_seconds():
            duration_delta = MAX_DURATION
        else:
            duration_delta = timedelta(seconds=duration_seconds)
        start_time = datetime.now()
        end_time = start_time + duration_delta

        silence = {
            "id": silence_id,
            "matchers": silence_matchers,
            "startsAt": start_time.isoformat(),
            "endsAt": end_time.isoformat(),
            "createdBy": user,
            "comment": "Acknowledge alert from Matrix",
        }

        try:
            async with self.session.post(
                f"{self.api_url}/silences", json=silence
            ) as response:
                response.raise_for_status()
                data = await response.json()
        except ClientError as e:
            raise AlertmanagerServerError(
                f"Cannot create silence for alert fingerprint {fingerprint}"
            ) from e

        self.cache.set(fingerprint, data["silenceID"], expire=duration_seconds)

        return data["silenceID"]

    async def delete_silence(self, silence_id: str) -> None:
        if self.session is None:
            raise AlertmanagerClientError("Alertmanager client is not started")

        silence = await self.get_silence(silence_id)

        silence_state = silence["status"]["state"]
        if silence_state == "expired":
            raise SilenceExpiredError(
                f"Cannot delete already expired silence with ID {silence_id}"
            )

        try:
            async with self.session.delete(
                f"{self.api_url}/silence/{silence_id}"
            ) as response:
                response.raise_for_status()
        except ClientError as e:
            raise AlertmanagerServerError(
                f"Cannot delete silence with ID {silence_id}"
            ) from e

    @staticmethod
    def _find_alert(fingerprint: str, alerts: List[AlertDict]) -> AlertDict:
        for alert in alerts:
            if alert["fingerprint"] == fingerprint:
                return alert
        raise AlertNotFoundError(f"Cannot find alert with fingerprint {fingerprint}")

    @staticmethod
    def _find_silence(silence_id: str, silences: List[SilenceDict]) -> SilenceDict:
        for silence in silences:
            if silence["id"] == silence_id:
                return silence
        raise SilenceNotFoundError(f"Cannot find silence with ID {silence_id}")

from __future__ import annotations

import logging
from typing import List

import prometheus_client
from aiohttp import ClientError, web, web_request
from aiohttp.abc import AbstractAccessLogger
from aiohttp_prometheus_exporter.handler import metrics
from aiohttp_prometheus_exporter.middleware import prometheus_middleware_factory
from diskcache import Cache
from nio.exceptions import LocalProtocolError, SendRetryError

from matrix_alertbot.alert import Alert, AlertRenderer
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.chat_functions import send_text_to_room
from matrix_alertbot.config import Config
from matrix_alertbot.errors import (
    AlertmanagerError,
    MatrixClientError,
    SilenceExtendError,
    SilenceNotFoundError,
)
from matrix_alertbot.matrix import MatrixClientPool

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


class AccessLogger(AbstractAccessLogger):
    def log(
        self,
        request: web_request.BaseRequest,
        response: web.StreamResponse,
        time: float,
    ) -> None:
        if request is None:
            remote_address = "-"
            request_info = "-"
            referer_header = "-"
            user_agent_header = "-"
        else:
            if request.remote is None:
                remote_address = "-"
            else:
                remote_address = request.remote

            request_info = (
                f"{request.method} {request.path_qs} "
                f"HTTP/{request.version.major}.{request.version.minor}"
            )

            referer_header = request.headers.get("Referer", "-")
            user_agent_header = request.headers.get("User-Agent", "-")

        self.logger.debug(
            f'{remote_address} "{request_info}" {response.status} '
            f'{response.body_length} "{referer_header}" "{user_agent_header}"'
        )


@routes.get("/health")
async def get_health(request: web_request.Request) -> web.Response:
    return web.Response(status=200)


@routes.post("/alerts/{room_id}")
async def create_alerts(request: web_request.Request) -> web.Response:
    data = await request.json()
    room_id = request.match_info["room_id"]

    config: Config = request.app["config"]

    if room_id not in config.allowed_rooms:
        logger.error(f"Cannot send alerts to room ID {room_id}.")
        return web.Response(
            status=401, body=f"Cannot send alerts to room ID {room_id}."
        )

    if "alerts" not in data:
        logger.error("Received data without 'alerts' key")
        return web.Response(status=400, body="Data must contain 'alerts' key.")

    alert_dicts = data["alerts"]

    if not isinstance(data["alerts"], list):
        alerts_type = alert_dicts.__class__.__name__
        logger.error(f"Received data with invalid alerts type '{alerts_type}'.")
        return web.Response(
            status=400, body=f"Alerts must be a list, got '{alerts_type}'."
        )

    logger.info(f"Received {len(alert_dicts)} alerts for room ID {room_id}: {data}")

    if len(data["alerts"]) == 0:
        return web.Response(status=400, body="Alerts cannot be empty.")

    alerts: List[Alert] = []
    for alert_dict in alert_dicts:
        try:
            alert = Alert.from_dict(alert_dict)
        except KeyError as e:
            logger.error(f"Cannot parse alert dict: {e}")
            return web.Response(status=400, body=f"Invalid alert: {alert_dict}.")

        alerts.append(alert)

    for alert in alerts:
        try:
            await create_alert(alert, room_id, request)
        except AlertmanagerError as e:
            logger.error(
                f"An error occured with Alertmanager when handling alert with fingerprint {alert.fingerprint}: {e}"
            )
            return web.Response(
                status=500,
                body=f"An error occured with Alertmanager when handling alert with fingerprint {alert.fingerprint}.",
            )
        except (SendRetryError, LocalProtocolError, ClientError) as e:
            logger.exception(
                f"Unable to send alert {alert.fingerprint} to Matrix room {room_id}",
                exc_info=e,
            )
            return web.Response(
                status=500,
                body=f"An error occured when sending alert with fingerprint '{alert.fingerprint}' to Matrix room.",
            )
        except MatrixClientError as e:
            logger.exception(
                f"Unable to send alert {alert.fingerprint} to Matrix room {room_id}",
                exc_info=e,
            )
            return web.Response(
                status=500,
                body=f"An error occured when sending alert with fingerprint '{alert.fingerprint}' to Matrix room.",
            )
        except Exception as e:
            logger.exception(
                f"Unable to send alert {alert.fingerprint} to Matrix room {room_id}",
                exc_info=e,
            )
            return web.Response(
                status=500,
                body=f"An exception occured when sending alert with fingerprint '{alert.fingerprint}' to Matrix room.",
            )

    return web.Response(status=200)


async def create_alert(
    alert: Alert, room_id: str, request: web_request.Request
) -> None:
    alertmanager_client: AlertmanagerClient = request.app["alertmanager_client"]
    alert_renderer: AlertRenderer = request.app["alert_renderer"]
    matrix_client_pool: MatrixClientPool = request.app["matrix_client_pool"]
    cache: Cache = request.app["cache"]
    config: Config = request.app["config"]

    if alert.match_all_labels(config.dm_filter_labels):
        logger.info("Found all DM filter labels in alert labels")
        if config.dm_select_label and config.dm_select_label not in alert.labels:
            logger.warning(
                f"Dismissing alert: Cannot find select label {config.dm_select_label} in alert labels"
            )
            return

        dm_select_value = alert.labels[config.dm_select_label]
        if dm_select_value not in config.dm_users:
            logger.warning(
                f"Dismissing alert: Cannot find user with label {config.dm_select_label}={dm_select_value}"
            )
            return

        user_id = config.dm_users[dm_select_value]
        if user_id not in matrix_client_pool.dm_rooms:
            logger.warning(
                f"Dismissing alert: Cannot find a matrix room for user {user_id}"
            )
            return
        room_id = matrix_client_pool.dm_rooms[user_id]

    if alert.firing:
        try:
            silence_id = await alertmanager_client.update_silence(alert.fingerprint)
            logger.debug(
                f"Extended silence ID {silence_id} for alert with fingerprint {alert.fingerprint}"
            )
            return
        except SilenceNotFoundError as e:
            logger.debug(
                f"Unable to extend silence for alert with fingerprint {alert.fingerprint}: {e}"
            )
            cache.delete(alert.fingerprint)
        except SilenceExtendError as e:
            logger.debug(
                f"Unable to extend silence for alert with fingerprint {alert.fingerprint}: {e}"
            )

    plaintext = alert_renderer.render(alert, html=False)
    html = alert_renderer.render(alert, html=True)

    if matrix_client_pool.matrix_client is not None:
        event = await send_text_to_room(
            matrix_client_pool.matrix_client, room_id, plaintext, html, notice=False
        )
        logger.info(
            f"Sent alert {alert.fingerprint} to room {room_id} with event ID {event.event_id}"
        )
    else:
        raise MatrixClientError("No matrix client available")

    if alert.firing:
        cache.set(event.event_id, alert.fingerprint, expire=config.cache_expire_time)
    else:
        cache.delete(alert.fingerprint)


class Webhook:
    def __init__(
        self,
        matrix_client_pool: MatrixClientPool,
        alertmanager_client: AlertmanagerClient,
        cache: Cache,
        config: Config,
    ) -> None:
        self.app = web.Application(logger=logger)
        self.app["matrix_client_pool"] = matrix_client_pool
        self.app["alertmanager_client"] = alertmanager_client
        self.app["config"] = config
        self.app["cache"] = cache
        self.app["alert_renderer"] = AlertRenderer(config.template_dir)
        self.app.add_routes(routes)

        prometheus_registry = prometheus_client.CollectorRegistry(auto_describe=True)
        self.app.middlewares.append(
            prometheus_middleware_factory(registry=prometheus_registry)
        )
        self.app.router.add_get("/metrics", metrics())

        self.runner = web.AppRunner(self.app, access_log_class=AccessLogger)

        self.config = config
        self.address = config.address
        self.port = config.port
        self.socket = config.socket

    async def start(self) -> None:
        await self.runner.setup()

        site: web.BaseSite
        if self.address and self.port:
            site = web.TCPSite(self.runner, self.address, self.port)
            logger.info(f"Listening on {self.address}:{self.port}")
        elif self.socket:
            site = web.UnixSite(self.runner, self.socket)
            logger.info(f"Listening on unix://{self.socket}")

        await site.start()

    async def close(self) -> None:
        await self.runner.cleanup()

from __future__ import annotations

import asyncio
import json
import logging
import os
import random
from asyncio.exceptions import TimeoutError
from typing import Dict, List, Optional, Tuple

from aiohttp import ClientConnectionError, ServerDisconnectedError
from diskcache import Cache
from nio import (
    AccountDataEvent,
    EphemeralEvent,
    Event,
    PresenceEvent,
    Response,
    RoomPreset,
    RoomVisibility,
    ToDeviceEvent,
)
from nio.client import AsyncClient, AsyncClientConfig
from nio.events import (
    InviteMemberEvent,
    KeyVerificationCancel,
    KeyVerificationKey,
    KeyVerificationMac,
    KeyVerificationStart,
    MegolmEvent,
    ReactionEvent,
    RedactionEvent,
    RoomMessageText,
    RoomMessageUnknown,
)
from nio.exceptions import LocalProtocolError, LocalTransportError
from nio.responses import (
    JoinedMembersError,
    LoginError,
    ProfileGetDisplayNameError,
    RoomCreateError,
    WhoamiError,
)

import matrix_alertbot.callback
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.config import AccountConfig, Config

logger = logging.getLogger(__name__)


class MatrixClientPool:
    def __init__(
        self, alertmanager_client: AlertmanagerClient, cache: Cache, config: Config
    ) -> None:
        self._lock = asyncio.Lock()
        self._matrix_clients: Dict[AccountConfig, AsyncClient] = {}
        self._accounts: List[AccountConfig] = []

        self._accounts = config.accounts
        for account in self._accounts:
            matrix_client = self._create_matrix_client(
                account, alertmanager_client, cache, config
            )
            self._matrix_clients[account] = matrix_client

        self.account = next(iter(self._accounts))
        self.matrix_client = self._matrix_clients[self.account]

        self.dm_rooms = {}

    def unactive_user_ids(self):
        active_user_id = self.account.id
        user_ids = []
        for account in self._accounts:
            user_id = account.id
            if active_user_id is not user_id:
                user_ids.append(user_id)
        return user_ids

    async def switch_active_client(
        self,
    ) -> Optional[Tuple[AsyncClient, AccountConfig]]:
        async with self._lock:
            for account in random.sample(self._accounts, len(self._accounts)):
                if account is self.account:
                    continue

                logger.info(
                    f"Bot {account.id} | Checking if matrix client is connected"
                )
                matrix_client = self._matrix_clients[account]
                try:
                    whoami = await matrix_client.whoami()
                    logged_in = not isinstance(whoami, WhoamiError)
                except Exception:
                    logged_in = False

                if logged_in:
                    self.account = account
                    self.matrix_client = matrix_client

                    logger.warning(
                        f"Bot {self.account.id} | Matrix client for homeserver {self.account.homeserver_url} selected as new leader."
                    )

                    return matrix_client, account

            if self.matrix_client.logged_in:
                logger.warning(
                    f"Bot {self.account.id} | No active Matrix client available, keeping Matrix client for {self.account.homeserver_url} as the leader."
                )
            else:
                logger.error(
                    f"Bot {self.account.id} | No active Matrix client connected."
                )
        return None

    async def close(self) -> None:
        for matrix_client in self._matrix_clients.values():
            await matrix_client.close()

    def _create_matrix_client(
        self,
        account: AccountConfig,
        alertmanager_client: AlertmanagerClient,
        cache: Cache,
        config: Config,
    ) -> AsyncClient:
        # Configuration options for the AsyncClient
        try:
            matrix_client_config = AsyncClientConfig(
                max_limit_exceeded=5,
                max_timeouts=3,
                store_sync_tokens=True,
                encryption_enabled=True,
            )
        except ImportWarning as e:
            logger.warning(e)
            matrix_client_config = AsyncClientConfig(
                max_limit_exceeded=5,
                max_timeouts=3,
                store_sync_tokens=True,
                encryption_enabled=False,
            )

        # Load credentials from a previous session
        if os.path.exists(account.token_file):
            with open(account.token_file, "r") as ifd:
                credentials = json.load(ifd)
                account.token = credentials["access_token"]
                account.device_id = credentials["device_id"]

        # Initialize the matrix client based on stored credentials
        matrix_client = AsyncClient(
            account.homeserver_url,
            account.id,
            device_id=account.device_id,
            store_path=config.store_dir,
            config=matrix_client_config,
        )

        # Set up event callbacks
        callbacks = matrix_alertbot.callback.Callbacks(
            matrix_client, alertmanager_client, cache, config, self
        )

        matrix_client.add_event_callback(callbacks.message, (RoomMessageText,))
        matrix_client.add_event_callback(
            callbacks.invite_event_filtered_callback, (InviteMemberEvent,)
        )
        # matrix_client.add_event_callback(callbacks.debug, (Event,))
        matrix_client.add_event_callback(callbacks.decryption_failure, (MegolmEvent,))
        matrix_client.add_event_callback(callbacks.reaction, (ReactionEvent,))
        matrix_client.add_event_callback(callbacks.redaction, (RedactionEvent,))
        matrix_client.add_event_callback(
            callbacks.unknown_message, (RoomMessageUnknown,)
        )
        matrix_client.add_to_device_callback(
            callbacks.key_verification_start, (KeyVerificationStart,)
        )
        matrix_client.add_to_device_callback(
            callbacks.key_verification_cancel, (KeyVerificationCancel,)
        )
        matrix_client.add_to_device_callback(
            callbacks.key_verification_confirm, (KeyVerificationKey,)
        )
        matrix_client.add_to_device_callback(
            callbacks.key_verification_end, (KeyVerificationMac,)
        )
        matrix_client.add_event_callback(callbacks.debug_room_event, (Event,))
        matrix_client.add_presence_callback(callbacks.debug_presence, (PresenceEvent,))
        matrix_client.add_ephemeral_callback(
            callbacks.debug_ephemeral, (EphemeralEvent,)
        )
        matrix_client.add_global_account_data_callback(
            callbacks.debug_account_data, (AccountDataEvent,)
        )
        matrix_client.add_room_account_data_callback(
            callbacks.debug_room_account_data, (AccountDataEvent,)
        )
        matrix_client.add_to_device_callback(
            callbacks.debug_to_device, (ToDeviceEvent,)
        )
        matrix_client.add_response_callback(callbacks.debug_response, (Response,))

        return matrix_client

    async def find_existing_dm_rooms(
        self, account: AccountConfig, matrix_client: AsyncClient, config: Config
    ) -> Dict[str, str]:
        unactive_user_ids = self.unactive_user_ids()
        dm_rooms = {}

        for room_id in matrix_client.rooms:
            if room_id in config.allowed_rooms:
                continue

            room_members_response = await matrix_client.joined_members(room_id)
            if isinstance(room_members_response, JoinedMembersError):
                logger.warning(
                    f"Bot {account.id} | Cannot get joined members for room {room_id}"
                )
                continue

            room_members = []
            for room_member in room_members_response.members:
                room_members.append(room_member.user_id)
            logger.info(
                f"Bot {account.id} | Found {len(room_members)} room members in {room_id}"
            )

            if len(room_members) > len(self._matrix_clients) + 1:
                continue

            all_accounts_in_room = True
            for user_id in unactive_user_ids:
                if user_id not in room_members:
                    all_accounts_in_room = False
            if not all_accounts_in_room:
                continue
            logger.info(f"Bot {account.id} | All matrix clients are in {room_id}")

            for room_member in room_members:
                if room_member not in config.dm_users.inverse:
                    continue

                if room_member in dm_rooms:
                    logger.warning(
                        f"Bot {account.id} | Found more than one direct room with user {room_member}: {room_id}"
                    )
                    continue

                dm_rooms[room_member] = room_id
                logger.info(
                    f"Bot {account.id} | Found direct room {room_id} with user {room_member}"
                )

        return dm_rooms

    async def create_dm_rooms(
        self, account: AccountConfig, matrix_client: AsyncClient, config: Config
    ) -> None:
        async with self._lock:
            if matrix_client is self.matrix_client:
                unactive_user_ids = self.unactive_user_ids()

                self.dm_rooms = await self.find_existing_dm_rooms(
                    account=account, matrix_client=matrix_client, config=config
                )
                for user_id in config.dm_users.inverse:
                    if user_id in self.dm_rooms:
                        continue

                    display_name_response = await matrix_client.get_displayname(user_id)
                    if isinstance(display_name_response, ProfileGetDisplayNameError):
                        error = display_name_response.message
                        logger.warning(
                            f"Bot {account.id} | Cannot fetch user name for {user_id}: {error}"
                        )
                        continue
                    user_name = display_name_response.displayname

                    if config.dm_room_title:
                        room_title = config.dm_room_title.format(user=user_name)
                    else:
                        room_title = None

                    logger.info(
                        f"Bot {account.id} | Creating direct room with user {user_id}"
                    )
                    invitations = unactive_user_ids + [user_id]
                    room_user_ids = invitations + [account.id]
                    power_levels = {"users": dict.fromkeys(room_user_ids, 100)}
                    create_room_response = await matrix_client.room_create(
                        visibility=RoomVisibility.private,
                        name=room_title,
                        invite=invitations,
                        is_direct=True,
                        preset=RoomPreset.private_chat,
                        power_level_override=power_levels,
                    )
                    if isinstance(create_room_response, RoomCreateError):
                        error = create_room_response.message
                        logger.warning(
                            f"Bot {account.id} | Cannot create direct room with user {user_id}: {error}"
                        )
                        continue

                    dm_room_id = create_room_response.room_id
                    if dm_room_id is None:
                        logger.warning(
                            f"Bot {account.id} | Cannot find direct room id with user {user_id}"
                        )
                        continue

                    logger.info(
                        f"Bot {account.id} | Created direct room {dm_room_id} with user {user_id}"
                    )
                    self.dm_rooms[user_id] = dm_room_id

    async def start(
        self,
        account: AccountConfig,
        config: Config,
    ):
        matrix_client = self._matrix_clients[account]

        # Keep trying to reconnect on failure (with some time in-between)
        # We switch homeserver after some retries
        while True:
            try:
                if account.device_id and account.token:
                    matrix_client.restore_login(
                        user_id=account.id,
                        device_id=account.device_id,
                        access_token=account.token,
                    )

                    # Sync encryption keys with the server
                    if matrix_client.should_upload_keys:
                        await matrix_client.keys_upload()
                else:
                    # Try to login with the configured username/password
                    try:
                        login_response = await matrix_client.login(
                            password=account.password,
                            device_name=config.device_name,
                        )

                        # Check if login failed
                        if isinstance(login_response, LoginError):
                            logger.error(
                                f"Bot {account.id} | Failed to login: {login_response.message}"
                            )
                            return False
                    except LocalProtocolError as error:
                        # There's an edge case here where the user hasn't installed the correct C
                        # dependencies. In that case, a LocalProtocolError is raised on login.
                        logger.fatal(
                            f"Bot {account.id} | Failed to login. Have you installed the correct dependencies? "
                            "https://github.com/poljar/matrix-nio#installation "
                            "Error: %s",
                            error,
                        )
                        return False

                    if isinstance(login_response, LoginError):
                        logger.fatal(
                            f"Bot {account.id} | Failed to login: {login_response.message}"
                        )
                        return False

                    # Save user's access token and device ID
                    # See https://stackoverflow.com/a/45368120
                    account_token_fd = os.open(
                        account.token_file,
                        flags=os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
                        mode=0o640,
                    )
                    with os.fdopen(account_token_fd, "w") as ofd:
                        json.dump(
                            {
                                "device_id": login_response.device_id,
                                "access_token": login_response.access_token,
                            },
                            ofd,
                        )

                    # Login succeeded!

                logger.info(f"Bot {account.id} | Logged in.")

                await matrix_client.sync(timeout=30000, full_state=True)

                await self.create_dm_rooms(
                    account=account, matrix_client=matrix_client, config=config
                )

                await matrix_client.sync_forever(timeout=30000, full_state=True)
            except (
                ClientConnectionError,
                LocalTransportError,
                ServerDisconnectedError,
                TimeoutError,
            ):
                await matrix_client.close()

                logger.warning(
                    f"Bot {account.id} | Matrix client disconnected, retrying in 15s..."
                )

                if len(self._accounts) > 1 and self.matrix_client is matrix_client:
                    logger.warning(
                        f"Bot {account.id} | Selecting another Matrix client as leader..."
                    )
                    await self.switch_active_client()

                # Sleep so we don't bombard the server with login requests
                await asyncio.sleep(15)
            finally:
                await matrix_client.close()

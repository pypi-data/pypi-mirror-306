from __future__ import annotations

import random
import unittest
from unittest.mock import AsyncMock, Mock, call, patch

import nio
from diskcache import Cache
from nio.api import RoomPreset, RoomVisibility
from nio.responses import (
    JoinedMembersError,
    JoinedMembersResponse,
    ProfileGetDisplayNameError,
    ProfileGetDisplayNameResponse,
    RoomCreateError,
    RoomCreateResponse,
)

import matrix_alertbot
import matrix_alertbot.matrix
from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.config import AccountConfig, BiDict, Config
from matrix_alertbot.matrix import MatrixClientPool


def mock_create_matrix_client(
    matrix_client_pool: MatrixClientPool,
    account: AccountConfig,
    alertmanager_client: AlertmanagerClient,
    cache: Cache,
    config: Config,
) -> nio.AsyncClient:
    fake_matrix_client = Mock(spec=nio.AsyncClient)
    fake_matrix_client.logged_in = True
    return fake_matrix_client


def mock_joined_members(room_id: str) -> JoinedMembersResponse | JoinedMembersError:
    fake_joined_members_response = Mock(spec=JoinedMembersResponse)
    if "dmroom" in room_id:
        fake_joined_members_response.members = [
            Mock(spec=nio.RoomMember, user_id="@fake_dm_user:example.com"),
            Mock(spec=nio.RoomMember, user_id="@fake_user:matrix.example.com"),
            Mock(spec=nio.RoomMember, user_id="@other_user:chat.example.com"),
        ]
    elif "!missing_other_user:example.com" == room_id:
        fake_joined_members_response.members = [
            Mock(spec=nio.RoomMember, user_id="@fake_dm_user:example.com"),
            Mock(spec=nio.RoomMember, user_id="@fake_user:matrix.example.com"),
        ]
    elif "!missing_dm_user:example.com" == room_id:
        fake_joined_members_response.members = [
            Mock(spec=nio.RoomMember, user_id="@fake_user:matrix.example.com"),
            Mock(spec=nio.RoomMember, user_id="@other_user:chat.example.com"),
        ]
    else:
        fake_joined_members_response = Mock(spec=JoinedMembersError)

    return fake_joined_members_response


class FakeAsyncClientConfig:
    def __init__(
        self,
        max_limit_exceeded: int,
        max_timeouts: int,
        store_sync_tokens: bool,
        encryption_enabled: bool,
    ) -> None:
        if encryption_enabled:
            raise ImportWarning()

        self.max_limit_exceeded = max_limit_exceeded
        self.max_timeouts = max_timeouts
        self.store_sync_tokens = store_sync_tokens
        self.encryption_enabled = encryption_enabled


class MatrixClientPoolTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        random.seed(42)

        self.fake_alertmanager_client = Mock(spec=AlertmanagerClient)
        self.fake_cache = Mock(spec=Cache)

        self.fake_account_config_1 = Mock(spec=AccountConfig)
        self.fake_account_config_1.id = "@fake_user:matrix.example.com"
        self.fake_account_config_1.homeserver_url = "https://matrix.example.com"
        self.fake_account_config_1.device_id = "ABCDEFGH"
        self.fake_account_config_1.token_file = "account1.token.secret"
        self.fake_account_config_2 = Mock(spec=AccountConfig)
        self.fake_account_config_2.id = "@other_user:chat.example.com"
        self.fake_account_config_2.homeserver_url = "https://chat.example.com"
        self.fake_account_config_2.device_id = "IJKLMNOP"
        self.fake_account_config_2.token_file = "account2.token.secret"
        self.fake_config = Mock(spec=Config)
        self.fake_config.store_dir = "/dev/null"
        self.fake_config.accounts = [
            self.fake_account_config_1,
            self.fake_account_config_2,
        ]
        self.fake_config.allowed_rooms = "!abcdefg:example.com"
        self.fake_config.dm_users = BiDict(
            {
                "a7b37c33-574c-45ac-bb07-a3b314c2da54": "@fake_dm_user:example.com",
                "cfb32a1d-737a-4618-8ee9-09b254d98fee": "@other_dm_user:example.com",
            }
        )
        self.fake_config.dm_room_title = "Alerts for {user}"

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool, "_create_matrix_client", autospec=True
    )
    async def test_init_matrix_client_pool(self, fake_create_matrix_client) -> None:
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_create_matrix_client.return_value = fake_matrix_client

        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        fake_create_matrix_client.assert_has_calls(
            [
                call(
                    matrix_client_pool,
                    self.fake_account_config_1,
                    self.fake_alertmanager_client,
                    self.fake_cache,
                    self.fake_config,
                ),
                call(
                    matrix_client_pool,
                    self.fake_account_config_2,
                    self.fake_alertmanager_client,
                    self.fake_cache,
                    self.fake_config,
                ),
            ]
        )

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertEqual(fake_matrix_client, matrix_client_pool.matrix_client)
        self.assertEqual(2, len(matrix_client_pool._accounts))
        self.assertEqual(2, len(matrix_client_pool._matrix_clients))

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool, "_create_matrix_client", autospec=True
    )
    async def test_unactive_user_ids(self, fake_create_matrix_client) -> None:
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_create_matrix_client.return_value = fake_matrix_client

        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        unactive_user_ids = matrix_client_pool.unactive_user_ids()

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertListEqual([self.fake_account_config_2.id], unactive_user_ids)

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool, "_create_matrix_client", autospec=True
    )
    async def test_close_matrix_client_pool(self, fake_create_matrix_client) -> None:
        fake_matrix_client = Mock(spec=nio.AsyncClient)
        fake_create_matrix_client.return_value = fake_matrix_client

        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        await matrix_client_pool.close()

        fake_matrix_client.close.assert_has_calls([(call(), call())])

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_switch_active_client(self, fake_create_matrix_client) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        fake_matrix_client_1 = matrix_client_pool.matrix_client
        await matrix_client_pool.switch_active_client()
        fake_matrix_client_2 = matrix_client_pool.matrix_client

        self.assertEqual(self.fake_account_config_2, matrix_client_pool.account)
        self.assertNotEqual(fake_matrix_client_2, fake_matrix_client_1)

        await matrix_client_pool.switch_active_client()
        fake_matrix_client_3 = matrix_client_pool.matrix_client

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertEqual(fake_matrix_client_3, fake_matrix_client_1)

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_switch_active_client_with_whoami_raise_exception(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        for fake_matrix_client in matrix_client_pool._matrix_clients.values():
            fake_matrix_client.whoami.side_effect = Exception

        fake_matrix_client_1 = matrix_client_pool.matrix_client
        await matrix_client_pool.switch_active_client()
        fake_matrix_client_2 = matrix_client_pool.matrix_client

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertEqual(fake_matrix_client_2, fake_matrix_client_1)

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_switch_active_client_with_whoami_error(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        for fake_matrix_client in matrix_client_pool._matrix_clients.values():
            fake_matrix_client.whoami.return_value = Mock(
                spec=nio.responses.WhoamiError
            )

        fake_matrix_client_1 = matrix_client_pool.matrix_client
        await matrix_client_pool.switch_active_client()
        fake_matrix_client_2 = matrix_client_pool.matrix_client

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertEqual(fake_matrix_client_2, fake_matrix_client_1)

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_switch_active_client_with_whoami_error_and_not_logged_in(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        for fake_matrix_client in matrix_client_pool._matrix_clients.values():
            fake_matrix_client.whoami.return_value = Mock(
                spec=nio.responses.WhoamiError
            )
            fake_matrix_client.logged_in = False

        fake_matrix_client_1 = matrix_client_pool.matrix_client
        await matrix_client_pool.switch_active_client()
        fake_matrix_client_2 = matrix_client_pool.matrix_client

        self.assertEqual(self.fake_account_config_1, matrix_client_pool.account)
        self.assertEqual(fake_matrix_client_2, fake_matrix_client_1)

    @patch.object(
        matrix_alertbot.matrix, "AsyncClientConfig", spec=nio.AsyncClientConfig
    )
    async def test_create_matrix_client(self, fake_async_client_config: Mock) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        matrix_client_1 = matrix_client_pool._matrix_clients[self.fake_account_config_1]
        self.assertEqual(self.fake_account_config_1.id, matrix_client_1.user)
        self.assertEqual(
            self.fake_account_config_1.device_id, matrix_client_1.device_id
        )
        self.assertEqual(
            self.fake_account_config_1.homeserver_url, matrix_client_1.homeserver
        )
        self.assertEqual(self.fake_config.store_dir, matrix_client_1.store_path)
        self.assertEqual(7, len(matrix_client_1.event_callbacks))
        self.assertEqual(5, len(matrix_client_1.to_device_callbacks))

        fake_async_client_config.assert_has_calls(
            [
                call(
                    max_limit_exceeded=5,
                    max_timeouts=3,
                    store_sync_tokens=True,
                    encryption_enabled=True,
                ),
                call(
                    max_limit_exceeded=5,
                    max_timeouts=3,
                    store_sync_tokens=True,
                    encryption_enabled=True,
                ),
            ]
        )

    @patch.object(
        matrix_alertbot.matrix,
        "AsyncClientConfig",
        spec=nio.AsyncClientConfig,
        side_effect=FakeAsyncClientConfig,
    )
    async def test_create_matrix_client_with_encryption_disabled(
        self, fake_async_client_config: Mock
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        matrix_client_1 = matrix_client_pool._matrix_clients[self.fake_account_config_1]
        self.assertEqual(self.fake_account_config_1.id, matrix_client_1.user)
        self.assertEqual(
            self.fake_account_config_1.device_id, matrix_client_1.device_id
        )
        self.assertEqual(
            self.fake_account_config_1.homeserver_url, matrix_client_1.homeserver
        )
        self.assertEqual(self.fake_config.store_dir, matrix_client_1.store_path)
        self.assertEqual(7, len(matrix_client_1.event_callbacks))
        self.assertEqual(5, len(matrix_client_1.to_device_callbacks))
        self.assertEqual(5, matrix_client_1.config.max_limit_exceeded)
        self.assertEqual(3, matrix_client_1.config.max_timeouts)
        self.assertTrue(matrix_client_1.config.store_sync_tokens)
        self.assertFalse(matrix_client_1.config.encryption_enabled)

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_find_existing_dm_rooms(self, fake_create_matrix_client) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.rooms = [
            "!abcdefg:example.com",
            "!fake_dmroom:example.com",
            "!missing_other_user:example.com",
            "!missing_dm_user:example.com",
            "!error:example.com",
        ]
        fake_matrix_client.joined_members.side_effect = mock_joined_members

        dm_rooms = await matrix_client_pool.find_existing_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.joined_members.assert_has_calls(
            [
                call("!fake_dmroom:example.com"),
                call("!missing_other_user:example.com"),
                call("!missing_dm_user:example.com"),
                call("!error:example.com"),
            ]
        )
        self.assertDictEqual(
            {"@fake_dm_user:example.com": "!fake_dmroom:example.com"}, dm_rooms
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_find_existing_dm_rooms_with_duplicates(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.rooms = [
            "!abcdefg:example.com",
            "!fake_dmroom:example.com",
            "!other_dmroom:example.com",
        ]
        fake_matrix_client.joined_members.side_effect = mock_joined_members

        dm_rooms = await matrix_client_pool.find_existing_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.joined_members.assert_has_calls(
            [
                call("!fake_dmroom:example.com"),
                call("!other_dmroom:example.com"),
            ]
        )
        self.assertDictEqual(
            {"@fake_dm_user:example.com": "!fake_dmroom:example.com"}, dm_rooms
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_create_dm_rooms(self, fake_create_matrix_client) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        fake_find_existing_dm_rooms = AsyncMock(autospec=True)
        fake_find_existing_dm_rooms.return_value = {
            "@other_dm_user:example.com": "!other_dmroom:example.com"
        }
        matrix_client_pool.find_existing_dm_rooms = fake_find_existing_dm_rooms

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.get_displayname.return_value = Mock(
            spec=ProfileGetDisplayNameResponse, displayname="FakeUser"
        )
        fake_room_create_response = Mock(spec=RoomCreateResponse)
        fake_room_create_response.room_id = "!fake_dmroom:example.com"
        fake_matrix_client.room_create.return_value = fake_room_create_response

        await matrix_client_pool.create_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.get_displayname.assert_called_once_with(
            "@fake_dm_user:example.com"
        )
        fake_matrix_client.room_create.assert_called_once_with(
            visibility=RoomVisibility.private,
            name="Alerts for FakeUser",
            invite=["@other_user:chat.example.com", "@fake_dm_user:example.com"],
            is_direct=True,
            preset=RoomPreset.private_chat,
            power_level_override={
                "users": {
                    "@fake_user:matrix.example.com": 100,
                    "@other_user:chat.example.com": 100,
                    "@fake_dm_user:example.com": 100,
                }
            },
        )
        self.assertDictEqual(
            {
                "@fake_dm_user:example.com": "!fake_dmroom:example.com",
                "@other_dm_user:example.com": "!other_dmroom:example.com",
            },
            matrix_client_pool.dm_rooms,
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_create_dm_rooms_with_empty_room_id(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        fake_find_existing_dm_rooms = AsyncMock(autospec=True)
        fake_find_existing_dm_rooms.return_value = {
            "@other_dm_user:example.com": "!other_dmroom:example.com"
        }
        matrix_client_pool.find_existing_dm_rooms = fake_find_existing_dm_rooms

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.get_displayname.return_value = Mock(
            spec=ProfileGetDisplayNameResponse, displayname="FakeUser"
        )
        fake_room_create_response = Mock(spec=RoomCreateResponse)
        fake_room_create_response.room_id = None
        fake_matrix_client.room_create.return_value = fake_room_create_response

        await matrix_client_pool.create_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.get_displayname.assert_called_once_with(
            "@fake_dm_user:example.com"
        )
        fake_matrix_client.room_create.assert_called_once_with(
            visibility=RoomVisibility.private,
            name="Alerts for FakeUser",
            invite=["@other_user:chat.example.com", "@fake_dm_user:example.com"],
            is_direct=True,
            preset=RoomPreset.private_chat,
            power_level_override={
                "users": {
                    "@fake_user:matrix.example.com": 100,
                    "@other_user:chat.example.com": 100,
                    "@fake_dm_user:example.com": 100,
                }
            },
        )
        self.assertDictEqual(
            {
                "@other_dm_user:example.com": "!other_dmroom:example.com",
            },
            matrix_client_pool.dm_rooms,
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_create_dm_rooms_with_empty_room_title(
        self, fake_create_matrix_client
    ) -> None:
        self.fake_config.dm_room_title = None

        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        fake_find_existing_dm_rooms = AsyncMock(autospec=True)
        fake_find_existing_dm_rooms.return_value = {
            "@other_dm_user:example.com": "!other_dmroom:example.com"
        }
        matrix_client_pool.find_existing_dm_rooms = fake_find_existing_dm_rooms

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.get_displayname.return_value = Mock(
            spec=ProfileGetDisplayNameResponse, displayname="FakeUser"
        )
        fake_room_create_response = Mock(spec=RoomCreateResponse)
        fake_room_create_response.room_id = "!fake_dmroom:example.com"
        fake_matrix_client.room_create.return_value = fake_room_create_response

        await matrix_client_pool.create_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.get_displayname.assert_called_once_with(
            "@fake_dm_user:example.com"
        )
        fake_matrix_client.room_create.assert_called_once_with(
            visibility=RoomVisibility.private,
            name=None,
            invite=["@other_user:chat.example.com", "@fake_dm_user:example.com"],
            is_direct=True,
            preset=RoomPreset.private_chat,
            power_level_override={
                "users": {
                    "@fake_user:matrix.example.com": 100,
                    "@other_user:chat.example.com": 100,
                    "@fake_dm_user:example.com": 100,
                }
            },
        )
        self.assertDictEqual(
            {
                "@fake_dm_user:example.com": "!fake_dmroom:example.com",
                "@other_dm_user:example.com": "!other_dmroom:example.com",
            },
            matrix_client_pool.dm_rooms,
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_create_dm_rooms_with_error(self, fake_create_matrix_client) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        fake_find_existing_dm_rooms = AsyncMock(autospec=True)
        fake_find_existing_dm_rooms.return_value = {
            "@other_dm_user:example.com": "!other_dmroom:example.com"
        }
        matrix_client_pool.find_existing_dm_rooms = fake_find_existing_dm_rooms

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.get_displayname.return_value = Mock(
            spec=ProfileGetDisplayNameResponse, displayname="FakeUser"
        )
        fake_room_create_response = Mock(spec=RoomCreateError)
        fake_room_create_response.message = "error"
        fake_matrix_client.room_create.return_value = fake_room_create_response

        await matrix_client_pool.create_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.get_displayname.assert_called_once_with(
            "@fake_dm_user:example.com"
        )
        fake_matrix_client.room_create.assert_called_once_with(
            visibility=RoomVisibility.private,
            name="Alerts for FakeUser",
            invite=["@other_user:chat.example.com", "@fake_dm_user:example.com"],
            is_direct=True,
            preset=RoomPreset.private_chat,
            power_level_override={
                "users": {
                    "@fake_user:matrix.example.com": 100,
                    "@other_user:chat.example.com": 100,
                    "@fake_dm_user:example.com": 100,
                }
            },
        )
        self.assertDictEqual(
            {
                "@other_dm_user:example.com": "!other_dmroom:example.com",
            },
            matrix_client_pool.dm_rooms,
        )

    @patch.object(
        matrix_alertbot.matrix.MatrixClientPool,
        "_create_matrix_client",
        autospec=True,
        side_effect=mock_create_matrix_client,
    )
    async def test_create_dm_rooms_with_display_name_error(
        self, fake_create_matrix_client
    ) -> None:
        matrix_client_pool = MatrixClientPool(
            alertmanager_client=self.fake_alertmanager_client,
            cache=self.fake_cache,
            config=self.fake_config,
        )
        fake_find_existing_dm_rooms = AsyncMock(autospec=True)
        fake_find_existing_dm_rooms.return_value = {
            "@other_dm_user:example.com": "!other_dmroom:example.com"
        }
        matrix_client_pool.find_existing_dm_rooms = fake_find_existing_dm_rooms

        fake_matrix_client = matrix_client_pool.matrix_client
        fake_matrix_client.get_displayname.return_value = Mock(
            spec=ProfileGetDisplayNameError, message="error"
        )
        fake_room_create_response = Mock(spec=RoomCreateResponse)
        fake_room_create_response.room_id = None
        fake_matrix_client.room_create.return_value = fake_room_create_response

        await matrix_client_pool.create_dm_rooms(
            account=matrix_client_pool.account,
            matrix_client=matrix_client_pool.matrix_client,
            config=self.fake_config,
        )

        fake_matrix_client.get_displayname.assert_called_once_with(
            "@fake_dm_user:example.com"
        )
        fake_matrix_client.room_create.assert_not_called()
        self.assertDictEqual(
            {
                "@other_dm_user:example.com": "!other_dmroom:example.com",
            },
            matrix_client_pool.dm_rooms,
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import logging
import os
import re
import sys
from typing import Any, Dict, List, Optional, TypeVar

import pytimeparse2
import yaml

from matrix_alertbot.errors import (
    InvalidConfigError,
    ParseConfigError,
    RequiredConfigKeyError,
)

logger = logging.getLogger()
logging.getLogger("peewee").setLevel(
    logging.INFO
)  # Prevent debug messages from peewee lib


DEFAULT_REACTIONS = {
    "🤫",
    "😶",
    "🤐",
    "🙊",
    "🔇",
    "🔕",
    "🚮",
    "⛔",
    "🚫",
    "🤬",
    "🫥",
    "😶‍🌫️",
    "🫣",
    "🫢",
    "😪",
    "😴",
    "💤",
    "🥱",
    "🤌",
    "🤏",
    "🤚",
    "👎",
    "🖕",
}

INSULT_REACTIONS = {
    "🤬",
    "🤌",
    "🖕",
}

K = TypeVar("K")
V = TypeVar("V")


class BiDict(dict[K, V]):
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, set()).add(key)

    def __setitem__(self, key: K, value: V):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(BiDict, self).__setitem__(key, value)
        self.inverse.setdefault(value, set()).add(key)

    def __delitem__(self, key: K):
        self.inverse.setdefault(self[key], set()).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(BiDict, self).__delitem__(key)


class AccountConfig:
    def __init__(self, account: Dict[str, str]) -> None:
        self.id: str = account["id"]
        if not re.match("@.+:.+", self.id):
            raise InvalidConfigError("matrix.user_id must be in the form @name:domain")

        self.password: Optional[str] = account.get("password")
        self.token: Optional[str] = account.get("token")

        if self.password is None and self.token is None:
            raise RequiredConfigKeyError("Must supply either user token or password")

        self.device_id: Optional[str] = account.get("device_id")
        self.token_file: str = account.get("token_file", "token.json")

        self.homeserver_url: str = account["url"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"


class Config:
    """Creates a Config object from a YAML-encoded config file from a given filepath"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.isfile(filepath):
            raise ParseConfigError(f"Config file '{filepath}' does not exist")

        # Load in the config file at the given filepath
        with open(filepath) as file_stream:
            self.config_dict = yaml.safe_load(file_stream.read())

        # Parse and validate config options
        self._parse_config_values()

    def _parse_config_values(self) -> None:
        """Read and validate each config option"""
        # Logging setup
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s [%(levelname)s] %(message)s"
        )

        # this must be DEBUG to allow debug messages
        # actual log levels are defined in the handlers below
        logger.setLevel("DEBUG")

        file_logging_enabled = self._get_cfg(
            ["logging", "file_logging", "enabled"], default=False
        )
        file_logging_filepath = self._get_cfg(
            ["logging", "file_logging", "filepath"], default="matrix-alertbot.log"
        )
        file_logging_log_level = self._get_cfg(
            ["logging", "file_logging", "level"], default="INFO"
        )
        if file_logging_enabled:
            file_handler = logging.FileHandler(file_logging_filepath)
            file_handler.setFormatter(formatter)
            if file_logging_log_level:
                file_handler.setLevel(file_logging_log_level)
            logger.addHandler(file_handler)

        console_logging_enabled = self._get_cfg(
            ["logging", "console_logging", "enabled"], default=True
        )
        console_logging_log_level = self._get_cfg(
            ["logging", "console_logging", "level"], default="INFO"
        )
        if console_logging_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            if console_logging_log_level:
                console_handler.setLevel(console_logging_log_level)
            logger.addHandler(console_handler)

        # Storage setup
        self.store_dir: str = self._get_cfg(["storage", "path"], required=True)

        # Create the store folder if it doesn't exist
        if not os.path.isdir(self.store_dir):
            if not os.path.exists(self.store_dir):
                os.mkdir(self.store_dir)
            else:
                raise InvalidConfigError(
                    f"storage.path '{self.store_dir}' is not a directory"
                )

        # Template setup
        self.template_dir: str = self._get_cfg(["template", "path"], required=False)

        # Cache setup
        self.cache_dir: str = self._get_cfg(["cache", "path"], required=True)
        expire_time: str = self._get_cfg(["cache", "expire_time"], default="1w")
        self.cache_expire_time = pytimeparse2.parse(expire_time)

        # Alertmanager client setup
        self.alertmanager_url: str = self._get_cfg(
            ["alertmanager", "url"], required=True
        )

        # Matrix bot accounts setup
        self.accounts: List[AccountConfig] = []
        accounts_dict: list = self._get_cfg(["matrix", "accounts"], required=True)
        for i, account_dict in enumerate(accounts_dict):
            try:
                account = AccountConfig(account_dict)
            except KeyError as e:
                key_name = e.args[0]
                raise RequiredConfigKeyError(
                    f"Config option matrix.accounts.{i}.{key_name} is required"
                )
            self.accounts.append(account)
        self.user_ids = {account.id for account in self.accounts}
        self.device_name: str = self._get_cfg(
            ["matrix", "device_name"], default="matrix-alertbot"
        )
        self.allowed_rooms: list = self._get_cfg(
            ["matrix", "allowed_rooms"], required=True
        )
        self.allowed_reactions = set(
            self._get_cfg(["matrix", "allowed_reactions"], default=DEFAULT_REACTIONS)
        )
        self.insult_reactions = set(
            self._get_cfg(["matrix", "insult_reactions"], default=INSULT_REACTIONS)
        )

        self.address: str = self._get_cfg(["webhook", "address"], required=False)
        self.port: int = self._get_cfg(["webhook", "port"], required=False)
        self.socket: str = self._get_cfg(["webhook", "socket"], required=False)
        if (
            not (self.address or self.port or self.socket)
            or (self.address and not self.port)
            or (not self.address and self.port)
        ):
            raise RequiredConfigKeyError(
                "Must supply either webhook.socket or both webhook.address and webhook.port"
            )
        elif self.socket and self.address and self.port:
            raise InvalidConfigError(
                "Supplied both webhook.socket and both webhook.address"
            )

        self.dm_users: BiDict[str, str] = BiDict()
        for user in self._get_cfg(["dm", "users"], default=[]):
            for select_value in user["select_values"]:
                self.dm_users[select_value] = user["matrix_id"]

        self.dm_room_title: str = self._get_cfg(["dm", "room_title"], required=False)
        filter_labels: Dict[str, str] = self._get_cfg(
            ["dm", "filter_labels"], default={}, required=False
        )
        self.dm_filter_labels: Dict[str, re.Pattern[str]] = {}
        for label_name, pattern in filter_labels.items():
            self.dm_filter_labels[label_name] = re.compile(pattern)

        self.dm_select_label: str = self._get_cfg(
            ["dm", "select_label"], required=False
        )

    def _get_cfg(
        self,
        path: List[str],
        default: Optional[Any] = None,
        required: bool = True,
    ) -> Any:
        """Get a config option from a path and option name, specifying whether it is
        required.

        Raises:
            RequiredConfigKeyError: If required is True and the object is not found (and there is
                no default value provided), a ConfigError will be raised.
        """
        # Sift through the the config until we reach our option
        config = self.config_dict
        for name in path:
            config = config.get(name)

            # If at any point we don't get our expected option...
            if config is None:
                # Raise an error if it was required
                if required and default is None:
                    raise RequiredConfigKeyError(
                        f"Config option {'.'.join(path)} is required"
                    )

                # or return the default value
                return default

        # We found the option. Return it.
        return config

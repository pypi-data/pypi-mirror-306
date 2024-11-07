import json
import logging
from os import environ, path
from typing import Any, Dict, List, Optional, Union

import yaml

from .node import Node
from .vault import Vault

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, files: Optional[List[str]] = None,
                 passkey: Optional[str] = None):
        self._files: List[str] = []
        self._configuration: Dict[str, Any] = {}
        self._passkey: Optional[bytes] = None

        if passkey:
            self._passkey = passkey.encode("utf-8")
        elif environ.get("VAULT_PASSKEY"):
            self._passkey = environ["VAULT_PASSKEY"].encode("utf-8")
        if files:
            for config_file in files:
                self.load(config_file)

    def reload(self):
        for config_file in self._files:
            self.load(config_file)

    def load(self, config_file: str, silent=False):
        logger.info("Trying to load configuration from: %s", config_file)
        if not path.exists(config_file):
            (logger.warn if silent else logger.critical)(
                "Missing config file: %s", config_file)
            if not silent:
                raise FileNotFoundError()
            return False
        if config_file.endswith((".yml", ".yaml")):
            self._parse_yml(config_file)
        elif config_file.endswith(".json"):
            self._parse_json(config_file)
        else:
            return False
        if config_file not in self._files:
            self._files.append(config_file)
        return True

    def find(self, path: str, default=None):
        cursor = self._configuration
        for key in path.split("."):
            if isinstance(cursor, dict) and key in cursor:
                cursor = cursor[key]
            else:
                return default
        return cursor

    def _parse_yml(self, config_file):
        with open(config_file) as fd:
            payload = fd.read()
        data = yaml.safe_load(self._strip_encrytion(payload))
        self._deep_update(data)

    def _parse_json(self, config_file):
        with open(config_file) as fd:
            payload = fd.read()
        data = json.loads(self._strip_encrytion(payload))
        self._deep_update(data)

    def _strip_encrytion(self, payload: str) -> str:
        if payload.startswith(Vault.prefix()):
            if self._passkey is None:
                raise RuntimeError("No decryption key provided")
            vault = Vault(self._passkey)
            decrypted = vault.decrypt(payload)
            return decrypted
        else:
            return payload

    def _deep_update(self, source: dict, target: Optional[dict] = None):
        if target is None:
            target = self._configuration
        if not source:
            return source
        for key, value in source.items():
            if isinstance(value, dict):
                if key not in target or not isinstance(target[key], dict):
                    target[key] = {}
                self._deep_update(value, target[key])
            else:
                target[key] = value

    def __getattribute__(self, attr: str):
        methods = ("reload", "load", "find")
        if attr.startswith("_") or attr in methods:
            return super().__getattribute__(attr)

        value: Union[Dict, Node, None] = self._configuration
        keys = attr.split(".")
        for key in keys:
            if value is not None and key in value:
                value = value[key]
                if not isinstance(value, dict):
                    return value
                value = Node(value)
            else:
                value = None
        return value

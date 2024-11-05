import json
import os
from functools import cached_property
from typing import Any, Dict, Optional

from snarkify_cli.lib.constants import CLI_CONFIG_FILE, PROJECT_CONFIG_FILE


class LazyLoadConfig:

    def __init__(self, config_path: str):
        self._config_path = os.path.expanduser(config_path)

    @cached_property
    def _data(self) -> Dict[str, str]:
        try:
            with open(self._config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def __getattribute__(self, name: str) -> Any:
        if name in type(self).__annotations__.keys():
            return self._data.get(name, None)
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: Any):
        if name in type(self).__annotations__.keys():
            self._data[name] = value
        else:
            super().__setattr__(name, value)

    def save(self):
        directory = os.path.dirname(self._config_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self._config_path, "w") as f:
            f.write(json.dumps(self._data))

    def remove(self):
        self._data.clear()
        os.remove(self._config_path)


class _CliConfig(LazyLoadConfig):
    api_key: Optional[str] = None
    team_id: Optional[str] = None

    def has_auth(self) -> bool:
        return self.api_key is not None


class _ProjectConfig(LazyLoadConfig):
    service_id: Optional[str] = None


CliConfig = _CliConfig(CLI_CONFIG_FILE)
ProjectConfig = _ProjectConfig(PROJECT_CONFIG_FILE)

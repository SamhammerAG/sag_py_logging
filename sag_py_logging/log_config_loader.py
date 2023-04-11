from abc import abstractmethod
from typing import Any, Dict


class LogLoader:
    @abstractmethod
    def __call__(self, log_template: str) -> Dict[str, Any]:
        pass  # pragma: no cover


class JsonLoader(LogLoader):
    def __init__(self) -> None:
        import json

        self.json = json

    def __call__(self, string_config: str) -> Dict[str, Any]:
        return self.json.loads(string_config)


class TomlLoader(LogLoader):
    def __init__(self) -> None:
        try:
            import tomli
        except ImportError as e:
            raise ModuleNotFoundError(
                "Module 'tomli' not installed.  Please run " "'python -m pip install sag-py-logging[toml]'"
            ) from e
        import tomli

        self.tomli = tomli

    def __call__(self, string_config: str) -> Dict[str, Any]:
        return self.tomli.loads(string_config)

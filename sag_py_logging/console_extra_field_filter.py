import json
import logging
from typing import Any, Dict, List, Set


class ConsoleExtraFieldFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name=name)
        self.excluded_standard_fields: Set[str] = {
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "id",
            "levelname",
            "levelno",
            "lineno",
            "message",
            "module",
            "msecs",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack_info",
            "thread",
            "threadName",
            "logsource",
            "program",
            "type",
            "tags",
            "@metadata",
            "color_message",
        }

    def filter(self, record: logging.LogRecord) -> bool:
        extra_fields: Dict[str, Any] = self._get_extra_fields(record)
        extra_list: List[str] = self._to_key_value_strings(extra_fields)
        record.stringified_extra = ", ".join(extra_list)
        return True

    def _get_extra_fields(self, record: logging.LogRecord) -> Dict[str, Any]:
        return {key: value for key, value in record.__dict__.items() if key not in self.excluded_standard_fields}

    def _to_key_value_strings(self, extra_fields: Dict[str, Any]) -> List[str]:
        return [f"{key}={json.dumps(value)}" for key, value in extra_fields.items()]

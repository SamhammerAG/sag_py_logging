import json
import logging
import logging.config
from string import Template
from typing import Any, Dict, Mapping


def init_logging(
    config_file: str, placeholder_container: Mapping[str, object], encoding: str = "UTF-8"
) -> Dict[str, Any]:
    with open(config_file, "r", encoding=encoding) as log_config_reader:
        log_template: str = log_config_reader.read()
        log_config_dict: Dict[str, Any] = _template_to_parsed_json(log_template, placeholder_container)
        _init_python_logging(log_config_dict)
        return log_config_dict


def _template_to_parsed_json(log_template: str, placeholder_container: Mapping[str, object]) -> Dict[str, Any]:
    parsed_log_templage: str = Template(log_template).substitute(placeholder_container)
    return json.loads(parsed_log_templage)


def _init_python_logging(log_config_dict: Dict[str, Any]) -> None:
    logging.basicConfig()
    logging.config.dictConfig(log_config_dict)

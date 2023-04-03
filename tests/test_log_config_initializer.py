from typing import Any, Dict, Mapping

import pytest

from sag_py_logging.log_config_initializer import _template_to_parsed_json


@pytest.fixture()
def test_template() -> str:
    return """{
        "version": 1,
        "disable_existing_loggers": "true",
        "root": {
            "handlers": ["myhandler"],
            "level": "INFO"
        },
        "handlers": {
            "myhandler": {
                "host": "${host}",
                "port": ${port},
                "formatter": "handler_formatter"
            }
        }
    }"""


def test__template_to_parsed_jsons__with_placeholders(test_template: str) -> None:
    # Arrange
    template_container: Mapping[str, object] = {"host": "myHost", "port": 1}

    # Act
    actual: Dict[str, Any] = _template_to_parsed_json(test_template, template_container)

    # Assert
    assert actual["version"] == 1
    assert actual["handlers"]["myhandler"]["host"] == "myHost"
    assert actual["handlers"]["myhandler"]["port"] == 1


def test__template_to_parsed_jsons__with_missing_placeholders(test_template: str) -> None:
    with pytest.raises(KeyError) as exception:
        # Arrange
        template_container: Mapping[str, object] = {"port": 1}

        # Act
        _template_to_parsed_json(test_template, template_container)

    # Assert
    assert str(exception) == "<ExceptionInfo KeyError('host') tblen=4>"

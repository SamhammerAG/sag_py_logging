import pytest

from sag_py_logging.log_config_loader import JsonLoader, TomlLoader


@pytest.fixture()
def test_json() -> str:
    return """{
        "version": 1,
        "disable_existing_loggers": true,
        "root": {
            "handlers": ["myhandler"],
            "level": "INFO"
        },
        "handlers": {
            "myhandler": {
                "formatter": "handler_formatter"
            }
        }
    }"""


@pytest.fixture()
def test_toml() -> str:
    return """version = 1
        disable_existing_loggers = true

        [root]
        handlers = [ "myhandler" ]
        level = "INFO"

        [handlers.myhandler]
        formatter = "handler_formatter"
    """


def test__json_loader(test_json: str) -> None:
    # Arrange
    json_loader = JsonLoader()

    # Act
    actual = json_loader(test_json)

    # Assert
    assert actual["version"] == 1
    assert actual["disable_existing_loggers"] == True
    assert actual["root"]["handlers"][0] == "myhandler"
    assert actual["root"]["level"] == "INFO"
    assert actual["handlers"]["myhandler"]["formatter"] == "handler_formatter"


def test__toml_loader(test_toml: str) -> None:
    # Arrange
    toml_loader = TomlLoader()

    # Act
    actual = toml_loader(test_toml)

    # Assert
    assert actual["version"] == 1
    assert actual["disable_existing_loggers"] == True
    assert actual["root"]["handlers"][0] == "myhandler"
    assert actual["root"]["level"] == "INFO"
    assert actual["handlers"]["myhandler"]["formatter"] == "handler_formatter"

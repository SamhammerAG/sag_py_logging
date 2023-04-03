from logging import INFO, LogRecord
from typing import cast

import pytest

from sag_py_logging import ConsoleExtraFieldFilter, ExtraFieldsLogRecord


@pytest.fixture()
def log_record() -> LogRecord:
    return LogRecord(name="", level=INFO, pathname="", lineno=0, msg="Hello, world!", args=(), exc_info=None)


def test_without_extra_fields(log_record: LogRecord) -> None:
    # Arrange
    filter_ = ConsoleExtraFieldFilter()

    # Act
    filter_.filter(log_record)

    # Assert
    assert cast(ExtraFieldsLogRecord, log_record).stringified_extra == ""


def test_with_extra_fields(log_record: LogRecord) -> None:
    # Arrange
    filter_ = ConsoleExtraFieldFilter()
    log_record.my_extra_string = "test"
    log_record.my_extra_int = 1
    log_record.my_extra_object = {"keyOne": "valueOne", "keyTwo": 2}

    # Act
    filter_.filter(log_record)

    # Assert
    assert (
        cast(ExtraFieldsLogRecord, log_record).stringified_extra
        == 'my_extra_string="test", my_extra_int=1, my_extra_object={"keyOne": "valueOne", "keyTwo": 2}'
    )

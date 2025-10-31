import logging
import os
from pathlib import Path

import pytest

import sag_py_logging.log_config_watcher as log_config_watcher


def write_toml(path: Path, content: str) -> None:
    path.write_text(content)
    os.utime(path, None)


def add_logger(logger_name: str, level: str) -> str:
    return f'[loggers."{logger_name}"]\nlevel = "{level}"\n'


@pytest.fixture(autouse=True)
def reset_logger_levels() -> None:
    logging.getLogger("access").setLevel(logging.NOTSET)
    logging.getLogger("other").setLevel(logging.NOTSET)


def test_override_changes_only_log_levels_in_override_file(tmp_path: Path) -> None:
    base = tmp_path / "base.toml"
    override = tmp_path / "override.toml"
    write_toml(base, add_logger("access", "WARNING") + add_logger("other", "WARNING"))
    write_toml(override, add_logger("access", "INFO"))

    log_config_watcher.build_and_apply_merged_config(base, override)

    assert logging.getLogger("access").level == logging.INFO
    assert logging.getLogger("other").level == logging.WARNING


def test_empty_override_level_is_ignored(tmp_path: Path) -> None:
    base = tmp_path / "base.toml"
    override = tmp_path / "override.toml"

    write_toml(base, add_logger("access", "ERROR"))
    write_toml(override, add_logger("access", ""))

    # The base file is never read (since we don't call init_logging). We have to manually set the access logger level first.
    logging.getLogger("access").setLevel("ERROR")

    log_config_watcher.build_and_apply_merged_config(base, override)

    assert logging.getLogger("access").level == logging.ERROR


def test_invalid_override_level_is_ignored(tmp_path: Path) -> None:
    base = tmp_path / "base.toml"
    override = tmp_path / "override.toml"

    write_toml(base, add_logger("access", "ERROR"))
    write_toml(override, add_logger("access", "NOTALEVEL"))

    # The base file is never read (since we don't call init_logging). We have to manually set the access logger level first.
    logging.getLogger("access").setLevel("ERROR")

    log_config_watcher.build_and_apply_merged_config(base, override)

    assert logging.getLogger("access").level == logging.ERROR


def test_reset_override_reverts_to_base(tmp_path: Path) -> None:
    base = tmp_path / "base.toml"
    override = tmp_path / "override.toml"
    write_toml(base, add_logger("access", "INFO"))
    write_toml(override, add_logger("access", "DEBUG"))

    log_config_watcher.build_and_apply_merged_config(base, override)
    assert logging.getLogger("access").level == logging.DEBUG

    # Reset file (which removes the access=DEBUG level)
    write_toml(override, add_logger("other", "WARNING"))
    log_config_watcher.build_and_apply_merged_config(base, override)

    assert logging.getLogger("access").level == logging.INFO

import logging
import time
from pathlib import Path
from threading import Thread
from typing import Any

import toml

logger = logging.getLogger(__name__)


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        logger.warning("Configfile for loglevels does not exist: %s", path)
        return {}
    return toml.loads(path.read_text())


def apply_level_overrides_from_toml(toml_obj: dict[str, Any]) -> None:
    for logger_key, logger_val in toml_obj.get("loggers", {}).items():
        name = logger_key
        level = None
        if isinstance(logger_val, dict):
            level = logger_val.get("level")
        if level:
            try:
                logger.info("adjusting attribute: %s, %s", logger_key, logger_val)
                lvl = getattr(logging, level.upper())
            except AttributeError:
                continue
            logging.getLogger(name if name != "root" else "").setLevel(lvl)


def build_and_apply_merged_config(base_path: Path, override_path: Path) -> None:
    base = load_toml(base_path)
    override = load_toml(override_path)
    if base == {} or override == {}:
        print("one of the logging config files for the watcher is empty, skipping")
        return
    merged = dict(base)
    merged_loggers = dict(base.get("loggers", {}))
    for k, v in override.get("loggers", {}).items():
        merged_loggers[k] = v
    if merged_loggers:
        merged["loggers"] = merged_loggers

    try:
        apply_level_overrides_from_toml(merged)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Skipping reload of logging config; invalid config or dictConfig failed: %s", exc)


def watch_override_file(base_path: Path, override_path: Path, poll_interval: int = 10) -> None:  # pragma: no cover
    last_mtime = None
    while True:
        try:
            mtime = override_path.stat().st_mtime if override_path.exists() else None
            if mtime != last_mtime:
                logger.debug("Log level change detected.")
                last_mtime = mtime
                build_and_apply_merged_config(base_path, override_path)
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning(
                "Unknown error occurred when trying to change log levels via override.toml."
                " Did you format the logging override.toml correctly? Exception: %s",
                exc,
            )
        time.sleep(poll_interval)


def start_logging_watcher(base_config_file: str, override_config_file: str) -> None:  # pragma: no cover
    print("starting logging.toml watcher")
    t = Thread(target=watch_override_file, args=(Path(base_config_file), Path(override_config_file)), daemon=True)
    t.start()

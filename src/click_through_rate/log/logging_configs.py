import json
import logging
import pathlib
from enum import StrEnum, auto
from logging.config import dictConfig

from click_through_rate.configs import project_configs


class EnvState(StrEnum):
    """Enum for the environment state."""

    DEV = auto()
    TEST = auto()
    PROD = auto()


env_to_log_level_map: dict[EnvState, int] = {
    EnvState.DEV: logging.DEBUG,
    EnvState.TEST: logging.DEBUG,
    EnvState.PROD: logging.INFO,
}

LOG_MESSAGE_TEMPLATE = "{class_name}.{function_name}: {message}"


def setup_logging() -> None:
    """Set up the logging configuration."""
    logging_config_file = pathlib.Path(__file__).parent.joinpath("logging_config.json")

    with open(logging_config_file, encoding=project_configs.encoding) as file:
        config = json.load(file)

    dictConfig(config)

    logging.getLogger().setLevel(env_to_log_level_map[project_configs.env_state])

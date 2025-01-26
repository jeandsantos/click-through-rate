"""Base class for settings objects."""

import json
import os
from typing import Any

from pydantic import BaseModel

from click_through_rate.components.settings_models import SettingsModel
from click_through_rate.configs import project_configs
from click_through_rate.log.project_logger import ProjectLogger


class Settings(ProjectLogger):
    """Settings for the project."""

    _settings_model: SettingsModel = SettingsModel

    def __init__(self) -> None:
        self.create_logger()
        self.model: SettingsModel | None = None

    def load_settings_from_file(self, filepath: os.PathLike) -> None:
        """Load settings from a file."""
        self.log_info(self.load_settings_from_file, f"Loading settings from {filepath}")

        with open(filepath, encoding=project_configs.encoding) as file:
            settings_dict = json.load(file)

        self.model = self._settings_model(**settings_dict)
        self.log_info(self.load_settings_from_file, "Successfully loaded settings from file")

    def load_settings_from_dict(self, settings_dict: dict[str, Any]) -> None:
        """Load settings from a dictionary."""
        self.log_info(self.load_settings_from_file, f"Loading settings from dictionary: {settings_dict}")
        self.model = self._settings_model(**settings_dict)
        self.log_info(self.load_settings_from_dict, "Successfully loaded settings from dict")

    def load_settings_from_model(self, settings_model: BaseModel) -> None:
        """Load settings from a dictionary."""
        self.log_info(self.load_settings_from_file, f"Loading settings from model: {settings_model}")
        self.model = settings_model
        self.log_info(self.load_settings_from_model, "Successfully loaded settings from model")

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from click_through_rate.enums import Environments

ENCODING_DEFAULT = "utf-8"
STORAGE_CLASS_DEFAULT = "STANDARD"


class ProjectConfigs(BaseSettings):
    """Class with project configurations."""

    encoding: str = ENCODING_DEFAULT
    env_state: Environments
    models_filepath: Path
    database_url: str
    google_application_credentials: str
    project_id: str = Field(description="GCP Project ID")
    location: str = Field(description="Location of GCS bucket")
    storage_class: str = Field(default=STORAGE_CLASS_DEFAULT, description="Storage class for items GCS in buckets")
    filepath_settings: Path

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding=ENCODING_DEFAULT)


project_configs = ProjectConfigs()

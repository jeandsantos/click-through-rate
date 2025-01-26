from pathlib import Path

from pydantic import BaseModel

from click_through_rate.components.settings import Settings


class DatabaseConnectionStringResource(BaseModel):
    database_url: str

    def get_connection_string(self) -> str:
        """Get the connection string to the database.

        Returns:
            str: The connection string to the database.

        """
        return f"duckdb://{self.database_url}"


class SettingsResource(BaseModel):
    filepath: str

    def get_settings(self) -> Settings:
        settings = Settings()
        settings.load_settings_from_file(Path(self.filepath))
        return settings


class ModelStorageResource(BaseModel):
    filepath: str

    def get_path(self) -> Path:
        return Path(self.filepath)

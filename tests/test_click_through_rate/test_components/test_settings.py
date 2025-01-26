from pathlib import Path

from click_through_rate.components.settings import Settings
from click_through_rate.components.settings_models import SettingsModel
from click_through_rate.constants import SEED


class TestSettings:
    def test_settings_instantiates(self):
        settings = Settings()
        assert settings.model is None

    def test_settings_loads_from_file(self, path_settings: Path):
        settings = Settings()
        result = settings.load_settings_from_file(path_settings)

        assert result is None
        assert settings.model is not None
        assert settings.model.seed == SEED
        assert isinstance(settings.model, SettingsModel)

    def test_settings_loads_from_dict(self, settings_dict: dict):
        settings = Settings()
        result = settings.load_settings_from_dict(settings_dict)

        assert result is None
        assert settings.model is not None
        assert settings.model.seed == SEED
        assert isinstance(settings.model, SettingsModel)

    def test_settings_loads_from_model(self, settings_model: SettingsModel):
        settings = Settings()
        result = settings.load_settings_from_model(settings_model)

        assert result is None
        assert settings.model is not None
        assert settings.model.seed == SEED
        assert isinstance(settings.model, SettingsModel)

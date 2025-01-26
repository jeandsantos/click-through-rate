import json
from pathlib import Path

from click_through_rate.components.settings_models import (
    FeatureEngineeringSettingsModel,
    IngestionSettingsModel,
    SettingsModel,
    TrainingSettingsModel,
)


class TestSettingsModel:
    def test_settings_model_instantiates_from_dict(self, project_path: Path):
        settings_dict = json.load(open(project_path.joinpath("settings.json")))

        result = SettingsModel(**settings_dict)

        assert isinstance(result, SettingsModel)
        assert isinstance(result.ingestion, IngestionSettingsModel)
        assert isinstance(result.feature_engineering, FeatureEngineeringSettingsModel)
        assert isinstance(result.training, TrainingSettingsModel)

        assert result.seed == settings_dict["seed"]
        assert result.verbose == settings_dict["verbose"]

import json
import shutil
from collections.abc import Generator
from pathlib import Path
from string import Template
from typing import Any

import pytest

from click_through_rate.components.settings_models import SettingsModel
from click_through_rate.resources import SettingsResource

PATH_SETTINGS: Path = Path(__file__).parent.joinpath("settings.json")
PATH_DATA: Path = Path(__file__).parent.joinpath("resources", "data")


settings_json_template = Template("""{
  "seed": 42,
  "verbose": false,
  "ingestion": {
    "filepaths": {
      "raw_train": "${raw_train_path}",
      "raw_test": "${raw_test_path}",
      "staged": "${staged_path}",
      "modelling": "${modelling_path}"
    },
    "cloud_storage": {
      "bucket_name": "ctr-prediction-raw",
      "project_id": "ctr-prediction",
      "train_blob_name": "train.gz",
      "test_blob_name": "test.gz"
    },
    "partitions": {
      "start_date": "2014-10-21",
      "end_date": "2014-10-30",
      "date_partition_format": "%Y-%m-%d"
    },
    "device_types": {
      "main": [
        "1"
      ],
      "other": [
        "0",
        "2",
        "3",
        "4",
        "5"
      ]
    }
  },
  "feature_engineering": {
    "categorical_rare_label_encoder": true,
    "categorical_impute_missing": true,
    "categorical_one_hot_encoder": true,
    "datetime_create_features": true,
    "all_drop_duplicate": true,
    "all_drop_constant": true,
    "all_drop_missing": true,
    "object_drop_columns": false,
    "standardize": true
  },
  "training": {
    "test_size": 0.2,
    "search_iterations": 20,
    "n_jobs": -1,
    "models": [
      "logistic_regression",
      "random_forest",
      "xgboost",
      "gradient_boosting_trees"
    ],
    "cross_validation": {
      "metric": "f1",
      "folds": 5,
      "scores": [
        "f1",
        "log_loss",
        "accuracy",
        "roc_auc",
        "recall"
      ]
    }
  }
}
""")


@pytest.fixture
def url_data():
    return "https://raw.githubusercontent.com/path/to/data.csv"


@pytest.fixture(scope="module")
def path_settings() -> Path:
    return PATH_SETTINGS


@pytest.fixture(scope="module")
def settings_dict(path_settings: Path) -> dict[str, Any]:
    return json.load(open(path_settings))


@pytest.fixture(scope="module")
def settings_model(settings_dict: dict) -> SettingsModel:
    return SettingsModel(**settings_dict)


@pytest.fixture(scope="module")
def path_data() -> Path:
    return PATH_DATA


@pytest.fixture(scope="module")
def settings_resource(path_settings: Path) -> SettingsResource:
    return SettingsResource(filepath=str(path_settings.absolute()))


@pytest.fixture
def project_path(
    tmp_path: Path,
    # path_settings: Path,
    path_data: Path,
) -> Generator[Path, None, None]:
    """Fixture that sets up a temporary project directory structure for testing.

    This fixture creates the necessary data directories and a settings JSON file
    in a temporary path. It also copies raw data files into the temporary data
    directory to simulate the project's data environment. The fixture yields the
    temporary path for use in tests and ensures cleanup by removing the temporary
    directory after the test execution completes.

    Yields:
        Path: The path to the temporary project directory.

    """
    # Create data directories
    tmp_path.joinpath("data").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "raw").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "staged").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "modelling").mkdir(parents=True, exist_ok=True)

    # Create settings JSON file
    template_values = {
        "raw_train_path": str(tmp_path.joinpath("data", "raw", "train.csv").absolute()),
        "raw_test_path": str(tmp_path.joinpath("data", "raw", "test.csv").absolute()),
        "staged_path": str(tmp_path.joinpath("data", "staged").absolute()),
        "modelling_path": str(tmp_path.joinpath("data", "modelling").absolute()),
    }
    json_str = settings_json_template.substitute(template_values)
    parsed_json = json.loads(json_str)

    json.dump(
        parsed_json,
        open(tmp_path.joinpath("settings.json"), "w"),
        indent=2,
    )

    # Copy raw data files
    shutil.copytree(
        path_data,
        tmp_path.joinpath("data"),
        dirs_exist_ok=True,
    )

    yield tmp_path

    shutil.rmtree(tmp_path)


@pytest.fixture
def project_path_no_data(
    tmp_path: Path,
    # path_settings: Path,
    path_data: Path,
) -> Generator[Path, None, None]:
    """Fixture that sets up a temporary project directory structure for testing.

    This fixture creates the necessary data directories and a settings JSON file
    in a temporary path. The fixture yields the temporary path for use in tests
    and ensures cleanup by removing the temporary directory after the test
    execution completes.

    Yields:
        Path: The path to the temporary project directory.

    """
    # Create data directories
    tmp_path.joinpath("data").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "raw").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "staged").mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath("data", "modelling").mkdir(parents=True, exist_ok=True)

    # Create settings JSON file
    template_values = {
        "raw_train_path": str(tmp_path.joinpath("data", "raw", "train.csv").absolute()),
        "raw_test_path": str(tmp_path.joinpath("data", "raw", "test.csv").absolute()),
        "staged_path": str(tmp_path.joinpath("data", "staged").absolute()),
        "modelling_path": str(tmp_path.joinpath("data", "modelling").absolute()),
    }
    json_str = settings_json_template.substitute(template_values)
    parsed_json = json.loads(json_str)

    json.dump(
        parsed_json,
        open(tmp_path.joinpath("settings.json"), "w"),
        indent=2,
    )

    yield tmp_path

    shutil.rmtree(tmp_path)


@pytest.fixture
def project_settings_resource(project_path: Path) -> SettingsResource:
    return SettingsResource(filepath=str(project_path.joinpath("settings.json").absolute()))


@pytest.fixture
def project_settings_resource_no_data(project_path_no_data: Path) -> SettingsResource:
    return SettingsResource(filepath=str(project_path_no_data.joinpath("settings.json").absolute()))

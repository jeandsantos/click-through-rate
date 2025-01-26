from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from click_through_rate.constants import SEED

MetricType = Literal["accuracy", "roc_auc", "precision", "recall", "f1", "log_loss"]
ModelType = Literal["logistic_regression", "random_forest", "xgboost", "gradient_boosting_trees"]


class IngestionFilePathsModel(BaseModel):
    raw_train: Path
    raw_test: Path
    staged: Path
    modelling: Path


class PartitionsModel(BaseModel):
    start_date: str
    end_date: str
    date_partition_format: str = "%Y-%m-%d"


class DeviceTypesModel(BaseModel):
    main: list[str] = Field(default=["1"])
    other: list[str] = Field(default=["0", "2", "3", "4", "5"])


class CloudStorageModel(BaseModel):
    project_id: str
    bucket_name: str
    train_blob_name: str
    test_blob_name: str


class IngestionSettingsModel(BaseModel):
    filepaths: IngestionFilePathsModel
    cloud_storage: CloudStorageModel
    partitions: PartitionsModel
    device_types: DeviceTypesModel


class FeatureEngineeringSettingsModel(BaseModel):
    """Model for feature engineering settings."""

    categorical_impute_missing: bool = True
    categorical_rare_label_encoder: bool = True
    categorical_one_hot_encoder: bool = True
    datetime_create_features: bool = False
    all_drop_duplicate: bool = True
    all_drop_constant: bool = True
    all_drop_missing: bool = True
    object_drop_columns: bool = False


class CrossValidationSettingsModel(BaseModel):
    """Model for cross-validation settings."""

    metric: MetricType
    folds: int = Field(ge=1, le=10)
    scores: list[MetricType]


class TrainingSettingsModel(BaseModel):
    """Model for training settings."""

    test_size: float = Field(gt=0, lt=1)
    search_iterations: int = Field(ge=1)
    n_jobs: int
    models: list[ModelType]
    cross_validation: CrossValidationSettingsModel


class SettingsModel(BaseModel):
    """Model for the settings of the train step.."""

    seed: int = Field(default=SEED)
    verbose: bool = Field(default=False)
    ingestion: IngestionSettingsModel
    feature_engineering: FeatureEngineeringSettingsModel
    training: TrainingSettingsModel

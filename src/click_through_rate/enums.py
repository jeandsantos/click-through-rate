from enum import StrEnum


class Environments(StrEnum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class DeviceCategory:
    """Types of device category."""

    MAIN = "main"
    OTHER = "other"


class SchemasClicks:
    """Schemas in the clicks database."""

    RAW = "raw"
    STAGED = "staged"
    CURATED = "curated"
    MODELLING = "modelling"


class TablesStaged:
    """Tables in the staging database."""

    F_INTERACTIONS = "f_interactions"
    D_DEVICES = "d_devices"
    D_SITES = "d_sites"
    D_APPS = "d_apps"


class TablesCurated:
    """Tables in the curated database."""

    TRAIN_DEVICES_MAIN = "train_devices_main"
    TRAIN_DEVICES_OTHER = "train_devices_other"


class TablesModelling:
    """Tables in the modelling database."""

    TRAIN = "train"
    TEST = "test"


class TrainRawData(StrEnum):
    """Columns of the `train_raw_data` asset."""

    ID = "id"
    CLICK = "click"
    HOUR = "hour"
    C1 = "c1"
    BANNER_POS = "banner_pos"
    SITE_ID = "site_id"
    SITE_DOMAIN = "site_domain"
    SITE_CATEGORY = "site_category"
    APP_ID = "app_id"
    APP_DOMAIN = "app_domain"
    APP_CATEGORY = "app_category"
    DEVICE_ID = "device_id"
    DEVICE_IP = "device_ip"
    DEVICE_MODEL = "device_model"
    DEVICE_TYPE = "device_type"
    DEVICE_CONN_TYPE = "device_conn_type"
    C14 = "c14"
    C15 = "c15"
    C16 = "c16"
    C17 = "c17"
    C18 = "c18"
    C19 = "c19"
    C20 = "c20"
    C21 = "c21"


class Transformers(StrEnum):
    CATEGORICAL_IMPUTE_MISSING = "categorical_impute_missing"
    CATEGORICAL_RARE_LABEL_ENCODER = "categorical_rare_label_encoder"
    CATEGORICAL_ONE_HOT_ENCODER = "categorical_one_hot_encoder"
    DATETIME_CREATE_FEATURES = "datetime_create_features"
    ALL_DROP_DUPLICATE = "all_drop_duplicate"
    ALL_DROP_CONSTANT = "all_drop_constant"
    ALL_DROP_MISSING = "all_drop_missing"
    ALL_REMOVE_CORRELATED = "all_remove_correlated"
    OBJECT_DROP_COLUMNS = "object_drop_columns"
    STANDARDIZE = "standardize"


class Metrics(StrEnum):
    """Enum for metrics available for evaluating models."""

    ACCURACY = "accuracy"
    ROC_AUC = "roc_auc"
    PRECISION = "precision"
    RECALL = "recall"
    F1 = "f1"
    LOG_LOSS = "log_loss"


METRIC_LOWER_IS_BETTER_MAP: dict[Metrics, bool] = {
    Metrics.ACCURACY: True,
    Metrics.ROC_AUC: True,
    Metrics.PRECISION: True,
    Metrics.RECALL: True,
    Metrics.F1: True,
    Metrics.LOG_LOSS: False,
}

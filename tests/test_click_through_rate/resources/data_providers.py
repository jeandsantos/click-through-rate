import random
from pathlib import Path

from faker import Faker
from mimesis import BaseDataProvider
from utils import generate_random_timestamps


class CustomDataProvider(BaseDataProvider):
    class Meta:
        name = "custom_provider"
        datadir = Path(__file__).parent / "schemas"

    def __init__(self):
        super().__init__()

    def generate_timestamps(self, *args, **kwargs):
        return generate_random_timestamps(*args, **kwargs)

    def generate_column_values(self, column_name: str, size: int = 1, *args, **kwargs):
        return self.random.choices(self._extract([column_name]), k=size, *args, **kwargs)

    def generate_values_from_list(self, values: list[str], size: int = 1, *args, **kwargs):
        return self.random.choices(values, k=size, *args, **kwargs)

    def generate_boolean_values(self, size: int = 1, *args, **kwargs):
        return self.random.choices([True, False], k=size, *args, **kwargs)


class StagedDataProvider(CustomDataProvider):
    class Meta:
        name = "custom_provider"
        datadir = Path(__file__).parent / "schemas"

    def __init__(self):
        super().__init__()
        Faker.seed(0)
        self.fake = Faker()

    def generate_ids(self, size: int = 1) -> list[str]:
        return ["100000" + str(self.fake.random_int(min=10**15, max=10**17 - 1)) for _ in range(size)]

    def generate_hex_ids(self, size: int = 1, length: int = 8, percent_unique: int = 100, *args, **kwargs) -> list[str]:
        if percent_unique < 0 or percent_unique > 100:  # noqa: PLR2004
            raise ValueError("percent_unique must be between 0 and 100")
        if percent_unique == 100:  # noqa: PLR2004
            return [self.fake.hexify(text="^" * length, *args, **kwargs) for _ in range(size)]

        unique_values = set()
        while len(unique_values) < size * percent_unique / 100:
            unique_values.add(self.fake.hexify(text="^" * length, *args, **kwargs))

        return random.choices(list(unique_values), k=size)

    def generate_hex_id(self, length: int = 8, *args, **kwargs) -> str:
        return self.fake.hexify(text="^" * length, *args, **kwargs)


class TrainDataProvider(CustomDataProvider):
    class Meta:
        name = "custom_provider"
        datadir = Path(__file__).parent / "schemas"

    def __init__(self, target_values: list[str] | None = None):
        super().__init__()
        self.target_values = target_values


class InteractionsDataProvider(StagedDataProvider):
    class Meta:
        name = "f_interactions"
        datafile = "f_interactions.json"
        datadir = Path(__file__).parent.joinpath("schemas")


class AppsDataProvider(StagedDataProvider):
    class Meta:
        name = "d_apps"
        datafile = "d_apps.json"
        datadir = Path(__file__).parent.joinpath("schemas")


class DevicesDataProvider(StagedDataProvider):
    class Meta:
        name = "d_devices"
        datafile = "d_devices.json"
        datadir = Path(__file__).parent.joinpath("schemas")


class SitesDataProvider(StagedDataProvider):
    class Meta:
        name = "d_sites"
        datafile = "d_sites.json"
        datadir = Path(__file__).parent.joinpath("schemas")


class TrainMainDataProvider(TrainDataProvider):
    class Meta:
        name = "train_main"
        datafile = "train_devices_main.json"
        datadir = Path(__file__).parent.joinpath("schemas")


class TrainOtherDataProvider(TrainDataProvider):
    class Meta:
        name = "train_other"
        datafile = "train_devices_other.json"
        datadir = Path(__file__).parent.joinpath("schemas")

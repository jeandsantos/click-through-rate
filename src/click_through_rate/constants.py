from pathlib import Path
from typing import Literal

CLIENT_API_URL = "http://localhost:8080/pipeline"
DATA_URL = "https://raw.githubusercontent.com/path/to/data.csv"

SEED: int = 42

DATE_PARTITION_FORMAT: str = "%Y-%m-%d"

START_DATE: str = "2014-10-21"
END_DATE: str = "2014-10-30"

TypeDevice = Literal["0", "1", "2", "3", "4", "5"]
DEVICE_TYPES_MAIN: list[TypeDevice] = ["1"]
DEVICE_TYPES_OTHER: list[TypeDevice] = ["0", "2", "3", "4", "5"]

COL_TARGET: str = "click"

PATH_DATA: Path = Path(__file__).parents[1].joinpath("data")
PATH_DATA_RAW: Path = PATH_DATA.joinpath("raw")
PATH_DATA_STAGED: Path = PATH_DATA.joinpath("staged")
PATH_DATA_MODEL: Path = PATH_DATA.joinpath("model")

TENACITY_DEFAULTS: dict[str, int] = {
    "start": 0,
    "increment": 5,
    "max": 300,
}

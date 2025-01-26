import json
import os
from pathlib import Path

import ibis
from utils import get_frequent_values

from click_through_rate.enums import SchemasClicks, TablesCurated, TablesStaged

COLS_TO_EXCLUDE_STAGED: list[str] = ["click", "timestamp", "id", "device_id", "device_ip", "site_id", "app_id"]
COLS_TO_EXCLUDE_CURATED: list[str] = ["click", "timestamp"]
MIN_PERCENTAGE_THRESHOLD: float = 1.0


def create_schemas(
    database_url: str,
    cols_to_exclude_staged: list[str] = COLS_TO_EXCLUDE_STAGED,
    cols_to_exclude_curated: list[str] = COLS_TO_EXCLUDE_CURATED,
    min_percentage_threshold: float = MIN_PERCENTAGE_THRESHOLD,
) -> None:
    """Create JSON schema files for specified tables in the staged and curated databases.

    This function connects to a DuckDB instance, retrieves the specified tables,
    and generates JSON schema files with frequent values for each column,
    excluding specified columns. The schemas are saved in the "schemas/en" directory.

    Parameters
    ----------
    database_url : str
        The URL of the DuckDB database to connect to.
    cols_to_exclude_staged : list[str], optional
        Columns to exclude when generating schemas for staged tables. Defaults to COLS_TO_EXCLUDE_STAGED.
    cols_to_exclude_curated : list[str], optional
        Columns to exclude when generating schemas for curated tables. Defaults to COLS_TO_EXCLUDE_CURATED.
    min_percentage_threshold : float, optional
        The minimum percentage threshold for a value to be considered frequent. Defaults to MIN_PERCENTAGE_THRESHOLD.

    Raises
    ------
    Exception
        If there is an error while creating the schema or saving the file.

    """
    for schema_name, table_name in [
        (SchemasClicks.STAGED, TablesStaged.F_INTERACTIONS),
        (SchemasClicks.STAGED, TablesStaged.D_DEVICES),
        (SchemasClicks.STAGED, TablesStaged.D_SITES),
        (SchemasClicks.STAGED, TablesStaged.D_APPS),
        (SchemasClicks.CURATED, TablesCurated.TRAIN_DEVICES_MAIN),
        (SchemasClicks.CURATED, TablesCurated.TRAIN_DEVICES_OTHER),
    ]:
        try:
            print(f"Creating schema for {schema_name}.{table_name}")
            con = ibis.connect(f"duckdb://{database_url}")

            cols_to_exclude = cols_to_exclude_staged if schema_name == SchemasClicks.STAGED else cols_to_exclude_curated
            table = con.table(table_name, database=schema_name)
            table_main_values_per_column = get_frequent_values(
                table,
                min_percentage=min_percentage_threshold,
                cols_exclude=cols_to_exclude,
            )

            filepath = Path(__file__).parent.joinpath(f"schemas/en/{table_name}.json")
            print(f"Saving schema for {schema_name}.{table_name} at {filepath.absolute()}")
            with open(filepath, "w") as file:
                json.dump(table_main_values_per_column, file, sort_keys=True, indent=4)

        finally:
            con.disconnect()


if __name__ == "__main__":
    create_schemas(database_url=os.getenv("DATABASE_URL"))

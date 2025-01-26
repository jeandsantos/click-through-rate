import json
import os
import pathlib
import random
import re
from pathlib import Path

import duckdb
import ibis
import pandas as pd
from data_providers import (
    AppsDataProvider,
    CustomDataProvider,
    DevicesDataProvider,
    InteractionsDataProvider,
    SitesDataProvider,
    StagedDataProvider,
    TrainDataProvider,
    TrainMainDataProvider,
    TrainOtherDataProvider,
)

from click_through_rate.assets.create_database import create_database
from click_through_rate.enums import SchemasClicks

N_ROWS: int = 1000
TIMESTAMP_END: str = "2014-01-01 00:00:00"
DIR_SCHEMAS: Path = Path(__file__).parent / "schemas" / "en"
PERCENTAGE_UNIQUE_IDS: int = 25
DB_FILE = Path(__file__).parent.joinpath("data", "clicks.db")


def convert_path_to_dot_notation(path_str: str):
    path_str_processed = pathlib.Path(path_str)
    return f"{path_str_processed.parts[-2:-1][0]}.{path_str_processed.stem}"


def load_parquet_to_duckdb(
    parquet_path: str,
    db_path: str,
    table_name: str,
    create_if_not_exists: bool = True,
) -> None:
    """Load a Parquet file into a DuckDB database.

    Args:
        parquet_path: Path to the Parquet file
        db_path: Path to the DuckDB database file
        table_name: Name of the table to create/insert into
        create_if_not_exists: Whether to create the table if it doesn't exist

    """
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    conn = duckdb.connect(db_path)

    try:
        if create_if_not_exists:
            conn.sql(f"""
                CREATE TABLE IF NOT EXISTS {table_name} AS
                SELECT * FROM read_parquet('{parquet_path}')
                WHERE 1=0
            """)

        conn.sql(f"""
            INSERT INTO {table_name}
            SELECT * FROM read_parquet('{parquet_path}')
        """)

        conn.commit()

    finally:
        conn.close()


def generate_staged_data() -> None:
    data_provider: StagedDataProvider = InteractionsDataProvider()
    schema: dict[str, str] = json.load(open(DIR_SCHEMAS.joinpath(data_provider.Meta.datafile)))

    fact_table = pd.DataFrame.from_dict(
        {"id": data_provider.generate_ids(size=N_ROWS)}
        | {"clicks": data_provider.generate_boolean_values(size=N_ROWS)}
        | {"timestamp": data_provider.generate_timestamps(size=N_ROWS, timestamp=TIMESTAMP_END, to_string=True)}
        | {column: data_provider.generate_column_values(column, size=N_ROWS) for column in schema.keys()}
        | {
            foreign_key: data_provider.generate_hex_ids(size=N_ROWS, length=8, percent_unique=PERCENTAGE_UNIQUE_IDS)
            for foreign_key in ["app_id", "device_id", "site_id"]
        }
    )

    fact_table.to_parquet(
        Path(__file__).parent.joinpath("data", "staged", f"{data_provider.Meta.name}.parquet"),
        index=False,
    )

    for data_provider_class in [AppsDataProvider, DevicesDataProvider, SitesDataProvider]:
        data_provider: CustomDataProvider = data_provider_class()
        schema: dict[str, str] = json.load(open(DIR_SCHEMAS.joinpath(data_provider.Meta.datafile)))
        col_id = re.sub(r"^d_|s$", "", data_provider.Meta.name) + "_id"

        dimension_table = pd.DataFrame.from_dict(
            {col_id: random.choices(fact_table[col_id], k=N_ROWS)}
            | {column: data_provider.generate_column_values(column, size=N_ROWS) for column in schema.keys()}
        )

        dimension_table.to_parquet(
            Path(__file__).parent.joinpath("data", "staged", f"{data_provider.Meta.name}.parquet"), index=False
        )


def generate_train_data() -> None:
    for data_provider_class in [TrainMainDataProvider, TrainOtherDataProvider]:
        data_provider: TrainDataProvider = data_provider_class()
        schema: dict[str, str] = json.load(open(DIR_SCHEMAS.joinpath(data_provider.Meta.datafile)))

        df = pd.DataFrame.from_dict(
            {"clicks": data_provider.generate_boolean_values(size=N_ROWS)}
            | {"timestamp": data_provider.generate_timestamps(size=N_ROWS, timestamp=TIMESTAMP_END, to_string=True)}
            | {
                column: data_provider.generate_column_values(column, size=N_ROWS)
                for column in schema.keys()
                if column not in ["click", "timestamp"]
            }
        )

        df.to_parquet(
            Path(__file__).parent.joinpath("data", "curated", f"{data_provider.Meta.name}.parquet"), index=False
        )


if __name__ == "__main__":
    generate_staged_data()
    generate_train_data()

    try:
        con: ibis.backends.duckdb.Backend = ibis.connect(f"duckdb://{DB_FILE}")
        try:
            print("Creating databases")
            for database_name in [
                SchemasClicks.RAW,
                SchemasClicks.STAGED,
                SchemasClicks.CURATED,
            ]:
                create_database(con, database_name, overwrite=True)
        except Exception as exception:
            print("Exception while creating databases", exception)
    finally:
        con.disconnect()

    dir_data = pathlib.Path(__file__).parent.joinpath("data")

    for filepath in dir_data.rglob("*.parquet"):
        table_name = convert_path_to_dot_notation(str(filepath))
        print(f"Loading {filepath.name} into table {table_name}")

        load_parquet_to_duckdb(
            filepath,
            db_path=DB_FILE,
            table_name=f"clicks.{table_name}",
            create_if_not_exists=True,
        )

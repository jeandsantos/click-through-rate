import os

import ibis
import ibis.backends.duckdb
from dotenv import load_dotenv

from click_through_rate import schemas
from click_through_rate.enums import SchemasClicks, TablesCurated, TablesStaged


def create_database(
    con: ibis.BaseBackend,
    database: str,
    overwrite: bool = False,
) -> None:
    if overwrite and (database in con.list_databases()):
        print(f"Dropping database {database}")
        for table in con.list_tables(database=database):
            con.drop_table(table, database=database, force=True)
        con.drop_database(database, force=True)

    print(f"Creating database {database}")
    con.create_database(database, force=True)


def create_tables(
    con: ibis.BaseBackend,
    database: str,
    tables: dict[str, dict[str, str]],
    overwrite: bool = False,
) -> None:
    for table_name, schema in tables.items():
        print(f"Creating table {table_name}")
        con.create_table(
            table_name,
            database=database,
            schema=schema,
            overwrite=overwrite,
        )


def create_clicks_databases_and_tables(con: ibis.BaseBackend) -> None:
    try:
        print("Creating databases")
        for database_name in [
            SchemasClicks.RAW,
            SchemasClicks.STAGED,
            SchemasClicks.CURATED,
            SchemasClicks.MODELLING,
        ]:
            create_database(con, database_name, overwrite=True)
    except Exception as e:
        print("Exception while creating databases", e)

    try:
        print("Creating tables")
        print("Creating tables for staged")
        create_tables(
            con,
            database=SchemasClicks.STAGED,
            tables={
                TablesStaged.F_INTERACTIONS: schemas.f_interactions,
                TablesStaged.D_DEVICES: schemas.d_devices,
                TablesStaged.D_SITES: schemas.d_sites,
                TablesStaged.D_APPS: schemas.d_apps,
            },
            overwrite=True,
        )

        print("Creating tables for curated")
        create_tables(
            con,
            database=SchemasClicks.CURATED,
            tables={
                TablesCurated.TRAIN_DEVICES_MAIN: schemas.train_devices_main,
                TablesCurated.TRAIN_DEVICES_OTHER: schemas.train_devices_other,
            },
            overwrite=True,
        )

    except Exception as e:
        print("Exception while creating tables", e)


if __name__ == "__main__":
    load_dotenv()
    con: ibis.backends.duckdb.Backend = ibis.connect(f"duckdb://{os.getenv('DATABASE_URL')}")

    try:
        create_clicks_databases_and_tables(con)
    finally:
        print("Closing connection")
        con.disconnect()

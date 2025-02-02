import os

from kfp import dsl

from click_through_rate.enums import Environment


@dsl.component(base_image="python:3.12")
def download_data():
    print("Downloading data.")


@dsl.pipeline
def ctr_pipeline():
    print("Running main script.")

    download_data_task = download_data()  # noqa: F841


if __name__ == "__main__":
    env = os.environ.get("ENVIRONMENT", default=Environment.DEV)

    if env == Environment.DEV:
        from kfp import local

        local.init(local.DockerRunner())

    ctr_pipeline()

import os

from dotenv import load_dotenv
from kfp import dsl

from click_through_rate.components.download_data import download_data
from click_through_rate.enums import Environment

download_data_component = dsl.component(download_data, base_image="python:3.12")


@dsl.pipeline
def ctr_pipeline():
    print("Running main script.")

    download_data_task = download_data_component()  # noqa: F841


if __name__ == "__main__":
    load_dotenv()
    env = os.environ.get("ENVIRONMENT")

    if env == Environment.DEV:
        from kfp import local

        local.init(local.DockerRunner())

    ctr_pipeline()

    from kfp.compiler import Compiler

    Compiler().compile(ctr_pipeline, "ctr_pipeline.yaml")

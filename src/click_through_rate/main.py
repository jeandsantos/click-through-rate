import datetime

from kfp import dsl

from click_through_rate.constants import CLIENT_API_URL, DATA_URL
from click_through_rate.utils.kfp_client_manager import KFPClientManager


@dsl.component(base_image="python:3.12")
def download_data(url: str) -> str:
    print(f"Downloading data from {url}")
    return url


@dsl.pipeline
def click_through_rate_pipeline(url: str) -> str:
    download_data_task = download_data(url=url)
    return download_data_task.output


def run_pipeline(url: str | None = None):
    print("Running main script.")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    kfp_client_manager = KFPClientManager(
        api_url=CLIENT_API_URL,
        skip_tls_verify=True,
        dex_username="user@example.com",
        dex_password="12341234",
        dex_auth_type="local",
    )

    # TIP: long-lived sessions might need to get a new client when their session expires
    kfp_client = kfp_client_manager.create_kfp_client()

    run = kfp_client.create_run_from_pipeline_func(
        pipeline_func=click_through_rate_pipeline,
        experiment_name="click-through-rate-experiment",
        run_name=f"click-through-rate-run-{ts}",
        namespace="kubeflow-user-example-com",
        arguments={"url": url if url is not None else DATA_URL},
    )

    print(run)


if __name__ == "__main__":
    run_pipeline(url=DATA_URL)

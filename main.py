from kfp import dsl

from kfp_client_manager import KFPClientManager


@dsl.component(base_image="python:3.12")
def say_hello(name: str) -> str:
    hello_text = f"Hello {name}!"
    print(hello_text)
    return hello_text


@dsl.pipeline
def hello_pipeline(recipient: str) -> str:
    hello_task = say_hello(name=recipient)
    return hello_task.output


def main():
    kfp_client_manager = KFPClientManager(
        api_url="http://localhost:8080/pipeline",
        skip_tls_verify=True,
        dex_username="user@example.com",
        dex_password="12341234",
        dex_auth_type="local",
    )

    # TIP: long-lived sessions might need to get a new client when their session expires
    kfp_client = kfp_client_manager.create_kfp_client()

    run = kfp_client.create_run_from_pipeline_func(
        pipeline_func=hello_pipeline,
        experiment_name="hello-world-experiment",
        namespace="kubeflow-user-example-com",
        arguments={
            "recipient": "World",
        },
    )

    print(run)


if __name__ == "__main__":
    main()

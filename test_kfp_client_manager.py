from kfp_client_manager import KFPClientManager

CLIENT_API_URL = "http://localhost:8080/pipeline"


def main():
    kfp_client_manager = KFPClientManager(
        api_url=CLIENT_API_URL,
        skip_tls_verify=True,
        dex_username="user@example.com",
        dex_password="12341234",
        dex_auth_type="local",
    )

    # TIP: long-lived sessions might need to get a new client when their session expires
    kfp_client = kfp_client_manager.create_kfp_client()

    experiments = kfp_client.list_experiments(namespace="kubeflow-user-example-com")
    print("\nexperiments")
    print(experiments)
    pipelines = kfp_client.list_pipelines(namespace="kubeflow-user-example-com")
    print("\npipelines")
    print(pipelines)
    runs = kfp_client.list_runs(namespace="kubeflow-user-example-com")
    print("\nruns")
    print(runs)


if __name__ == "__main__":
    main()

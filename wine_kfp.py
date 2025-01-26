from kfp import dsl

from kfp_client_manager import KFPClientManager


@dsl.component(
    base_image="python:3.12",
    packages_to_install=["pandas==2.2.3", "requests==2.32.3"],
)
def download_dataset(
    url: str,
    dataset: dsl.Output[dsl.Dataset],
):
    import io

    import pandas as pd
    import requests

    print(f"Downloading model from URL: {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    print("Converting the response content to a Pandas DataFrame")
    df = pd.read_csv(io.StringIO(resp.text), header=0, sep=";")
    print("Successfully created Pandas dataset")

    df.to_csv(dataset.path, index=False)


@dsl.component(
    base_image="python:3.12",
    packages_to_install=["pandas==2.2.3"],
)
def preprocess_dataset(
    dataset: dsl.Input[dsl.Dataset],
    preprocessed_dataset: dsl.Output[dsl.Dataset],
):
    import pandas as pd

    df = pd.read_csv(dataset.path)
    print("Preprocessing the DataFrame by standardizing column names")
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    df.to_csv(preprocessed_dataset.path, index=False)


@dsl.component(
    base_image="python:3.12",
    packages_to_install=["pandas==2.2.3", "scikit-learn==1.5.2"],
)
def train_model(
    dataset: dsl.Input[dsl.Dataset],
    hyper_parameters: dict,
    model: dsl.Output[dsl.Model],
):
    import pickle

    import pandas as pd
    from sklearn.linear_model import ElasticNet
    from sklearn.model_selection import train_test_split

    TARGET_COLUMN = "quality"
    SEED = 42

    df = pd.read_csv(dataset.path)

    print("Splitting the data into training and testing sets")
    train_x, test_x, train_y, test_y = train_test_split(
        df.drop(columns=[TARGET_COLUMN]),
        df[TARGET_COLUMN],
        test_size=0.25,
        random_state=SEED,
        stratify=df[TARGET_COLUMN],
    )
    classifier = ElasticNet(
        alpha=hyper_parameters["alpha"],
        l1_ratio=hyper_parameters["l1_ratio"],
        random_state=SEED,
    )
    print(f"Starting training process with the following hyper params: {hyper_parameters}")

    classifier.fit(train_x, train_y)
    score = classifier.score(test_x, test_y)
    print(f"Successfully trained the model, model accuracy is: {score}")

    with open(model.path, "wb") as f:
        pickle.dump(classifier, f)

    model.metadata["alpha"] = hyper_parameters["alpha"]
    model.metadata["l1_ratio"] = hyper_parameters["l1_ratio"]
    model.metadata["score"] = score


@dsl.pipeline
def mlops_pipeline(dataset_url: str):
    download_dataset_task = download_dataset(url=dataset_url)
    preprocess_dataset_task = preprocess_dataset(dataset=download_dataset_task.outputs["dataset"])

    hyper_parameters = {
        "alpha": 0.5,
        "l1_ratio": 0.5,
    }

    train_model_task = train_model(
        dataset=preprocess_dataset_task.outputs["preprocessed_dataset"],
        hyper_parameters=hyper_parameters,
    )


def main():
    DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    CLIENT_API_URL = "http://localhost:8080/pipeline"

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
        pipeline_func=mlops_pipeline,
        experiment_name="mlops-pipeline-20250123",
        namespace="kubeflow-user-example-com",
        arguments={
            "dataset_url": DATASET_URL,
        },
    )

    print(run)

    from kfp.compiler import Compiler

    Compiler().compile(mlops_pipeline, "mlops_pipeline.yaml")


if __name__ == "__main__":
    main()

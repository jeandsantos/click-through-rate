import pytest


@pytest.fixture(scope="session", autouse=True)
def docker_runner():
    """Initialize the Docker runner for tests using kfp"""
    from kfp import local

    local.init(local.DockerRunner())

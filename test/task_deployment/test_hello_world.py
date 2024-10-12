import os
import pytest
import swan
import time
import requests
from dotenv import load_dotenv

from swan import Orchestrator
from swan.object import TaskDeploymentInfo, TaskCreationResult, Task

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
WALLET_ADDRESS = os.getenv('WALLET')
PRIVATE_KEY = os.getenv('PK')


@pytest.fixture(scope="module")
def swan_orchestrator() -> Orchestrator:
    return swan.resource(
        api_key=API_KEY,
        network='testnet',
        service_name='Orchestrator'
    )


@pytest.fixture(scope="module")
def task_uuid(swan_orchestrator) -> str:
    result: TaskCreationResult = swan_orchestrator.create_task(
        app_repo_image="hello_world",
        wallet_address=WALLET_ADDRESS,
        private_key=PRIVATE_KEY,
        instance_type="C1ae.medium",
        auto_pay=True,
    )

    assert result.task_uuid is not None
    assert result.instance_type == 'C1ae.medium'

    return result['task_uuid']


def test_create_task(swan_orchestrator, task_uuid):
    assert task_uuid is not None
    assert isinstance(task_uuid, str)


def test_get_deployment_info(swan_orchestrator, task_uuid):
    task_info: TaskDeploymentInfo = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)

    assert isinstance(task_info, TaskDeploymentInfo)
    assert isinstance(task_info.task, Task)
    assert task_info is not None
    assert task_info.task.status is not None


@pytest.fixture(scope="module")
def real_url(swan_orchestrator, task_uuid) -> str:
    max_retries = 10
    retry_interval = 30  # seconds

    for _ in range(max_retries):
        job_urls = swan_orchestrator.get_real_url(task_uuid)

        if job_urls:
            assert isinstance(job_urls, list)
            assert len(job_urls) > 0
            return job_urls[0]

        time.sleep(retry_interval)

    pytest.fail("Failed to get real URL after maximum retries")


def test_hello_world_content(real_url: str):
    max_retries = 10
    retry_interval = 30  # seconds

    for _ in range(max_retries):
        response = requests.get(real_url)
        if response.status_code == 200:
            assert "Hello World" in response.text
            return
        time.sleep(retry_interval)

    pytest.fail("Failed to test the deployed app content after maximum retries")


if __name__ == "__main__":
    pytest.main([__file__])
import os

import pytest
from dotenv import load_dotenv
from loguru import logger

from tools.openapi.client import OpenAPIClient
from tools.openapi.task import TaskStatus
from tools.openapi.urls import FOTOR_OPENAPI_TXT2IMG_URL, FOTOR_OPENAPI_TASK_STATUS_URL, FOTOR_OPENAPI_VALIDATE_API_KEY

# Load environment variables from .env file
load_dotenv()
SANDBOX_API_KEY = os.getenv('SANDBOX_API_KEY')
SANDBOX_MODE = os.getenv('SANDBOX_MODE', '1')

FOTOR_ENDPOINT = "https://api-b.fotor.com"
if SANDBOX_MODE == '1':
    # Set the endpoint name
    FOTOR_ENDPOINT = "https://api-b-sandbox.fotor.com"


def test_get_version_info():
    client = OpenAPIClient(
        api_key=SANDBOX_API_KEY,
        create_task_url=FOTOR_ENDPOINT + FOTOR_OPENAPI_TXT2IMG_URL,
        get_task_status_url=FOTOR_ENDPOINT + FOTOR_OPENAPI_TASK_STATUS_URL,
        validate_api_key_url=FOTOR_ENDPOINT + FOTOR_OPENAPI_VALIDATE_API_KEY,
    )

    if not client.validate_api_key():
        logger.error("Invalid API key")
        return
    logger.info("API key is valid")

    payload = {
        "content": "a flying bird",
        "sizeId": "1:1",
        "templateId": "6b8d16cf-9402-4c22-b1e8-39eccce3436b",
        "negativePrompt": ""
    }

    logger.debug(f"Request payload={payload}")

    try:
        task = client.create_task(
            payload=payload,
        )
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return

    task = client.polling_task_status(task)
    if task.status == TaskStatus.COMPLETED:
        logger.debug(f"Task completed successfully: {task}")
        return

    elif task.status == TaskStatus.FAILED:
        logger.debug(f"Task failed: {task}")
        return

    elif task.status == TaskStatus.TIMEOUT:
        logger.debug(f"Task timed out: {task}")
        return


if __name__ == '__main__':
    pytest.main()

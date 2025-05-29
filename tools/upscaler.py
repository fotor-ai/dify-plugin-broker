from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from loguru import logger

from tools.openapi.client import OpenAPIClient
from tools.openapi.task import TaskStatus
from tools.openapi.urls import FOTOR_OPENAPI_UPSCALER_URL, FOTOR_OPENAPI_TASK_STATUS_URL


class UpscalerTool(Tool):
    """
    Tool to upscale image.
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        client = OpenAPIClient(
            api_key=self.runtime.credentials['fotor_openapi_key'],
            create_task_url=self.runtime.credentials['fotor_openapi_endpoint'] + FOTOR_OPENAPI_UPSCALER_URL,
            get_task_status_url=self.runtime.credentials['fotor_openapi_endpoint'] + FOTOR_OPENAPI_TASK_STATUS_URL,
        )

        payload = {
            "upscaling_resize": tool_parameters.get("upscaling_resize", 2),
            "userImageUrl": tool_parameters.get("userImageUrl"),
            "max_image_width": tool_parameters.get("max_image_width", 2048),
            "max_image_height": tool_parameters.get("max_image_height", 2048),
        }

        logger.debug(f"Request payload={payload}")

        try:
            task = client.create_task(
                payload=payload,
            )
        except Exception as e:
            logger.error(f"Failed to create task, error={e}")
            yield self.create_text_message(f"Error: Failed to create task.")
            raise e

        try:
            task = client.polling_task_status(task)
        except Exception as e:
            logger.error(f"Failed to polling task status, error={e}")
            yield self.create_text_message(f"{e}")
            raise e

        if task.status == TaskStatus.COMPLETED:
            logger.info(f"Task completed, task_id={task.id}, result_url={task.output}")
            yield self.create_image_message(task.output)
            yield self.create_variable_message(variable_name="result_url", variable_value=task.output)
            return

        elif task.status == TaskStatus.FAILED:
            logger.error(f"Task failed, task_id={task.id}")
            yield self.create_text_message("Error: Task failed.")
            raise Exception(f"{task.to_json()}")

        elif task.status == TaskStatus.TIMEOUT:
            logger.error(f"Task timeout, task_id={task.id}")
            yield self.create_text_message("Error: Task timeout.")
            raise Exception(f"{task.to_json()}")

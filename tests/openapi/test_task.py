import json

import pytest

from tools.openapi.task import Task, TaskType, TaskStatus


def test_print_task_info():
    task = Task(
        task_id="123",
        task_type=TaskType.GENERAL,
        task_input={
            "url": "https://example.com/123.png",
            "payload": {
                "demo1": "1",
                "demo2": 2,
            },
        },
        status=TaskStatus.FAILED,
    )
    json_task = json.dumps(task.print(), indent=4)
    print(f"task={json_task}")


if __name__ == '__main__':
    pytest.main()

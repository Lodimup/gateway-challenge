"""
Celery task queue scheduler for long running tasks
"""

from celery import Celery
from services.env_man import ENVS

TASK_ANNOTATIONS = {
    "tasks.ocrs.ocr": {
        "rate_limit": "10/s"
    },  # change to embedding and check actual rate limit
}
INCLUDE = ["tasks.ocrs"]


app = Celery(
    "tasks",
    broker=ENVS["CELERY_BROKER"],
    backend=ENVS["CELERY_BACKEND"],
    include=INCLUDE,
    task_annotations=TASK_ANNOTATIONS,
)


if __name__ == "__main__":
    app.start()

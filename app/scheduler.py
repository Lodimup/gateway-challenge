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
app.conf.update(
    task_concurrency=4,  # allows 4 tasks to run concurrently per worker
    worker_prefetch_multiplier=1,  # allows 1 task to be prefetched per worker
)


if __name__ == "__main__":
    app.start()

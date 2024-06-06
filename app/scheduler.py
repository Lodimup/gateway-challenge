"""
Celery task queue scheduler for long running tasks
TASK_ANNOTATIONS:
- rate_limit: limits the number of tasks that can be executed per second
to avoid external service rate limit
"""

from celery import Celery
from services.env_man import ENVS

TASK_ANNOTATIONS = {
    "tasks.ocrs.mock_ocr_and_embed_to_pc": {"rate_limit": "10/s"},
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
    task_concurrency=1,  # allows x tasks to run concurrently per worker
    worker_prefetch_multiplier=1,  # allows 1 task to be prefetched per worker
)


if __name__ == "__main__":
    app.start()

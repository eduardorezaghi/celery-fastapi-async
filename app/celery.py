import os

from celery import Celery

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "pyamqp://guest@localhost:5672//"
)
CELERY_BACKEND_URL = os.getenv(
    "CELERY_BACKEND_URL", "redis://localhost:6379/0"
)

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    celery_app.start()

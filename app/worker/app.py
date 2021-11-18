from celery import Celery

from app import config

celery_app = Celery(
    "app-worker",
    broker=config.CELERY_BROKER_URI,
)

celery_app.conf.worker_send_task_events = True

celery_app.autodiscover_tasks(["app.worker.tasks.*"])

celery_app.conf.beat_schedule = {}
celery_app.conf.timezone = "UTC"

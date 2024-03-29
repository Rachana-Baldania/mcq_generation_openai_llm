from celery import Celery
from app.core.configuration import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_BROKER_URL

celery.conf.timezone = "UTC"

celery.conf.update(
    {
        "task_routes": {
            "worker.schedule_task": {"queue": "beat-queue"},
        }
    }
)

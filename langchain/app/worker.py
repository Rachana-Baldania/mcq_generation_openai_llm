import time

from app.core.celery_app import celery
from app.core.configuration import settings


@celery.task(name="test_celery")
def test_celery(word: str) -> str:
    time.sleep(5)
    return f"test task return {word}"


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60, test_celery.s("hello from Scheduled Task"), name="test task"
    )

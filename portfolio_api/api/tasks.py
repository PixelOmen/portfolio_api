import logging
from celery import shared_task


@shared_task
def beat_task():
    logging.info("Beat Task")
    return "Beat Task Done"


@shared_task(bind=True)
def debug_task(self):
    logging.info(f'Request: {self.request!r}')
    return "Debug Task Done"

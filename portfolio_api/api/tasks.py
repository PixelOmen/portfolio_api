from celery import shared_task

# change to logger


@shared_task(bind=True)
def beat_task():
    print("Beat Task")
    return "Beat Task Done"


@shared_task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return "Debug Task Done"

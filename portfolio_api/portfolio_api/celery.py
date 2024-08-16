from celery import Celery
from django.conf import settings

celery_app = Celery('portfolio_api')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


TEST_SCHEDULE = {
    'task_every_hour': {
        'task': 'portfolio_api.tasks.beat_task',
        'schedule': 10.0,
    },
}

celery_app.conf.beat_schedule = TEST_SCHEDULE

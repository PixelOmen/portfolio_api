from celery import Celery
from celery.schedules import crontab

celery_app = Celery("portfolio_api")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


USER_DATA_RESET_SCHEDULE = {
    "user_data_reset_task": {
        "task": "core.tasks.user_data_reset_task",
        "schedule": crontab(minute="0", hour="0"),
    },
}

# ---- Debug ------
# USER_DATA_RESET_SCHEDULE = {
#     "user_data_reset_task": {
#         "task": "core.tasks.user_data_reset_task",
#         "schedule": 30,
#     },
# }

celery_app.conf.beat_schedule = USER_DATA_RESET_SCHEDULE

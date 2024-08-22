import sys
from .base import *

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY_DEV")

ALLOWED_HOSTS = [
    ".eacosta.dev",
    "eacosta.dev",
    "eaportfolio-alb-dev-1082017843.us-west-2.elb.amazonaws.com",
]

CORS_ALLOWED_ORIGINS = [
    "https://eacosta.dev",
    "https://dev.eacosta.dev",
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB_NAME"),
        "USER": env("POSTGRES_DB_USER"),
        "PASSWORD": env("POSTGRES_DB_PASSWORD"),
        "HOST": env("POSTGRES_DB_HOST_DEV"),
        "PORT": env("POSTGRES_DB_PORT"),
    }
}

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL_DEV")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_DEV")

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s: %(levelname)s/%(processName)s] %(name)s: %(message)s",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "celery.beat": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

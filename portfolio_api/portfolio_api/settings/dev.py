import os
import sys
import logging
import requests
from .base import *

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY_DEV")

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

# Allowed Hosts and CORS
ALLOWED_HOSTS = [
    ".eacosta.dev",
    "eacosta.dev",
]

CORS_ALLOWED_ORIGINS = [
    "https://eacosta.dev",
    "https://dev.eacosta.dev",
]

# Add the ECS container IP to allowed hosts
# (Needs to be after logging to log dynamic hosts)
django_logger = logging.getLogger("django")
METADATA_URI = os.environ.get("ECS_CONTAINER_METADATA_URI")
if METADATA_URI:
    try:
        container_metadata = requests.get(METADATA_URI).json()
    except Exception as e:
        django_logger.error(f"Error fetching container metadata: {e}")
    else:
        ALLOWED_HOSTS.append(container_metadata["Networks"][0]["IPv4Addresses"][0])
else:
    django_logger.warning(
        "ECS_CONTAINER_METADATA_URI env var not set, make sure this is not an ECS task for the API"
    )

import os
import sys
import logging
import requests
from .base import *

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY_STAGE")

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB_NAME"),
        "USER": env("POSTGRES_DB_USER"),
        "PASSWORD": env("POSTGRES_DB_PASSWORD"),
        "HOST": env("POSTGRES_DB_HOST_STAGE"),
        "PORT": env("POSTGRES_DB_PORT"),
    }
}

# DRFSO2
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = env("GOOGLE_OAUTH2_REDIRECT_URI_STAGE")

# AWS S3 Media Storage
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME_STAGE")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME_STAGE")

AWS_S3_FILE_OVERWRITE = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("DJANGO_CACHE_STAGE"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Channels
CL_HOST, CL_PORT, CL_DB = env("CHANNEL_LAYERS_REDIS_STAGE").split(":")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(CL_HOST, int(CL_PORT), int(CL_DB))],
        },
    },
}

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL_STAGE")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_STAGE")

# Email
EMAIL_PORTFOLIO_LINK = env("EMAIL_PORTFOLIO_LINK_STAGE")
EMAIL_LOGO_URL = env("EMAIL_LOGO_URL_STAGE")

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
        "googleauth": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
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
    "https://stage.eacosta.dev",
]

CSRF_TRUSTED_ORIGINS = ["https://stage.eacosta.dev"]

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
        try:
            container_ip = container_metadata["Networks"][0]["IPv4Addresses"][0]
        except (KeyError, IndexError) as e:
            django_logger.error(
                f"Error parsing container IP address from metadata response: {e}"
            )
        else:
            if container_ip not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(container_ip)
else:
    django_logger.warning(
        "ECS_CONTAINER_METADATA_URI env var not set, make sure this is not an ECS task for the API"
    )

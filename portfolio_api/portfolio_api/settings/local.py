import sys

from .base import *

DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY_DEV")

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB_NAME"),
        "USER": env("POSTGRES_DB_USER"),
        "PASSWORD": env("POSTGRES_DB_PASSWORD"),
        "HOST": env("POSTGRES_DB_HOST_LOCAL"),
        "PORT": env("POSTGRES_DB_PORT"),
    }
}

# DRFSO2
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = env("GOOGLE_OAUTH2_REDIRECT_URI_LOCAL")

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

# AWS S3 Media Storage
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID_LOCAL")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY_LOCAL")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME_DEV")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME_DEV")

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


# Email
EMAIL_PORTFOLIO_LINK = env("EMAIL_PORTFOLIO_LINK_DEV")
EMAIL_LOGO_URL = env("EMAIL_LOGO_URL_DEV")

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL_LOCAL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_LOCAL")

# Loggers
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

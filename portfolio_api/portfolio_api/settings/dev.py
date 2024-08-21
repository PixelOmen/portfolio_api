import sys

from .base import *

DEBUG = False

SECRET_KEY = env('DJANGO_SECRET_KEY_DEV')

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB_NAME'),
        'USER': env('POSTGRES_DB_USER'),
        'PASSWORD': env('POSTGRES_DB_PASSWORD'),
        'HOST': env('POSTGRES_DB_HOST_DEV'),
        'PORT': env('POSTGRES_DB_PORT'),
    }
}

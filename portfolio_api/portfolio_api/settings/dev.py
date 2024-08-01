from .base import *


DEBUG = True

SECRET_KEY = env('DJANGO_SECRET_KEY_DEV')

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DRFSO2
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = env('GOOGLE_OAUTH2_REDIRECT_URI_DEV')

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

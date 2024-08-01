from .base import *


DEBUG = False

# SECRET_KEY = env('DJANGO_SECRET_KEY_PROD')

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {}
}

# DRFSO2
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = env('GOOGLE_OAUTH2_REDIRECT_URI_PROD')

# CORS
CORS_ALLOWED_ORIGINS = [

]

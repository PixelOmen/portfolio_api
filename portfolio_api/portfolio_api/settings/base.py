from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Channels,
    "channels",
    # S3 storage
    "storages",
    # CORS
    "corsheaders",
    # DRF
    "rest_framework",
    # DRFSO2
    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",
    # Scheduling - Celery Beat
    "django_celery_beat",
    # Apps
    "core",
    "api",
    "socialauth",
    "cmdutils",
    "wschat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # CORS
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # DRFSO2, only needed for compatibility reasons
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_api.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DRF and DRFSO2 settings

AUTH_USER_MODEL = "socialauth.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drf_social_oauth2.authentication.SocialAuthentication",
    )
}

# User Limits
USER_LIMITS = {
    "DEFAULT_ALLOWED_IMAGE_MIMES": [
        "image/jpeg",
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/tiff",
        "image/tiff",
        "image/bmp",
        "image/webp",
        "image/svg+xml",
    ],
    "DEFAULT_MAX_IMAGE_SIZE": 5242880,
    "DEFAULT_MAX_USER_IMAGES": 10,
    "DEFAULT_MAX_POST_LENGTH": 200,
    "DEFAULT_MAX_CHAT_MESSAGES": 10,
}

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "drf_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Static (mainly for admin/drf)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

# OpenAI API Key
OPENAI_API_KEY = env("DJANGO_OPENAI_API_KEY")

# Google Base Settings (redirect in dev/prod settings)
SOCIAL_AUTH_GOOGLE_AUTHCODE_TOKEN_URL = "https://oauth2.googleapis.com/token"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_OAUTH2_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


# Superuser
DEFAULT_SUPERUSER_USERNAME = env("DJANGO_DEFAULT_SUPERUSER_USERNAME")
DEFAULT_SUPERUSER_EMAIL = env("DJANGO_DEFAULT_SUPERUSER_EMAIL")
DEFAULT_SUPERUSER_PASSWORD = env("DJANGO_DEFAULT_SUPERUSER_PASSWORD")

# Celery
CELERY_ACKS_LATE = True
CELERY_TIMEZONE = "America/Los_Angeles"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD").strip('"')
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
CONTACT_EMAIL = env("CONTACT_EMAIL")

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv("DJANGO_DEBUG", True) == "False" else True

allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", [])
ALLOWED_HOSTS = allowed_hosts.split(",") if allowed_hosts else []

# For Paypal integration testing
ALLOWED_HOSTS.append("ef47-2601-249-8c00-4a80-bdfa-78f-bdaa-6fd2.ngrok.io")

PAYPAL_TEST = True if os.getenv("PAYPAL_TEST") == "True" else False
if PAYPAL_TEST:
    PAYPAL_RECEIVER_EMAIL = "americanhandelsociety-facilitator@gmail.com"
    PAYPAL_ACTION_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
else:
    PAYPAL_RECEIVER_EMAIL = "americanhandelsociety@gmail.com"
    PAYPAL_ACTION_URL = "https://www.paypal.com/cgi-bin/webscr"

INSTALLED_APPS = [
    "americanhandelsociety_app.apps.AmericanHandelSocietyAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fontawesome-free",
    "paypal.standard.ipn",
    "captcha",
]

CAPTCHA_2X_IMAGE = True
CAPTCHA_BACKGROUND_COLOR = "transparent"
CAPTCHA_IMAGE_SIZE = [150, 75]
CAPTCHA_FONT_SIZE = 40

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "americanhandelsociety.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "americanhandelsociety.wsgi.application"


PSQL_DATABASE_NAME = "americanhandelsociety_postgres"
PSQL_USER = "ahs_admin"
PSQL_PASSWORD = "gfhandel"
PSQL_HOST = "127.0.0.1"

DATABASES = {}

DATABASES["default"] = dj_database_url.parse(
    os.getenv(
        "DATABASE_URL",
        f"postgres://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:5432/{PSQL_DATABASE_NAME}",
    ),
    conn_max_age=600,
    ssl_require=True if os.getenv("POSTGRES_REQUIRE_SSL") else False,
    engine="django.db.backends.postgresql",
)

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

AUTH_USER_MODEL = "americanhandelsociety_app.Member"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Preserve default loggers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "%B %-d, %Y"

DATETIME_FORMAT = "%B %-d, %Y, %-I:%M"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "americanhandelsociety_app/static"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

from pathlib import Path

from .settings import *


PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "americanhandelsociety-facilitator@gmail.com"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "american_handel_society",
        "USER": "ahs_admin",
        "PASSWORD": "gfhandel",
        "HOST": "127.0.0.1",
        "PORT": "5433",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = None
STATICFILES_STORAGE = None

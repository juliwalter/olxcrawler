import os
from olxcrawler.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []  # TODO: Add allowed hists

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "olxcrawler",
        "USER": os.environ.get("DB_USER", None),
        "PASSWORD": os.environ.get("DB_PASSWORD", None),
        "HOST": "127.0.0.1",  # TODO: Add prod host
        "PORT": "5432",  # TODO: Add prod port
    }
}

# django-apscheduler settings
# https://apscheduler.readthedocs.io/en/3.x/userguide.html
SCHEDULER_DEFAULT = True

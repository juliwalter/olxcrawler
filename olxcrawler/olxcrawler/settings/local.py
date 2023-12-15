from olxcrawler.settings.base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ox0e$_crf^($-&@%42u_@wbqtq9j6cyh#o=c5eh0p!o=mt*r(9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "olxcrawler",
        "USER": "dev",
        "PASSWORD": "dev",
        "HOST": os.uname().nodename,
        "PORT": "3306",
    },
}

# django-apscheduler settings
# https://apscheduler.readthedocs.io/en/3.x/userguide.html

SCHEDULER_DEFAULT = True

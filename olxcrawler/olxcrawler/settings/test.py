from olxcrawler.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ox0e$_crf^($-&@%42u_@wbqtq9j6cyh#o=c5eh0p!o=mt*r(9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test-database',
    }
}

# django-apscheduler settings
# https://apscheduler.readthedocs.io/en/3.x/userguide.html
SCHEDULER_DEFAULT = False

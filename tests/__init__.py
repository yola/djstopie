import os

from django.conf import settings


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
settings._setup()

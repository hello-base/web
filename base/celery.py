# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery
from configurations import importer
from dotenv import read_dotenv

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

# Read our `.env` for development purposes (which is now a directory up),
# then initialize django-configurations.
try:
    env = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    with open(env):
        read_dotenv(env)
except IOError:
    pass
importer.install()

# Initialize Celery and tell it we have some apps.
app = Celery('base')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

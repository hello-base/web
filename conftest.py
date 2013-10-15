import os
import sys

from django import get_version
from django.conf import settings


def pytest_report_header(config):
    return 'django: ' + get_version()


def pytest_configure():
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'
        os.environ['DJANGO_CONFIGURATION'] = 'Testing'

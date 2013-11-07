import os

from django import get_version
from django.conf import settings


def pytest_report_header(config):
    return 'django: ' + get_version()


def pytest_configure():
    import dotenv
    dotenv.read_dotenv()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'
    os.environ['DJANGO_CONFIGURATION'] = 'Testing'

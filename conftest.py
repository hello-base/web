import os

from django import get_version

from configurations import importer
from dotenv import read_dotenv


def pytest_report_header(config):
    return 'django: ' + get_version()


def pytest_configure(config):
    dotenv.read_dotenv()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'
    os.environ['DJANGO_CONFIGURATION'] = 'Testing'
    importer.install()

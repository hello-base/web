import os
import sys

from django import get_version

from configurations import importer
from dotenv import read_dotenv


def pytest_report_header(config):
    return 'django: ' + get_version()


def pytest_configure(config):
    # Make sure we have `base/` in our path.
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(path, 'base'))

    # If we have an .env file, read it.
    read_dotenv()

    # Specifiy our settings locations, then initialize them.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'
    os.environ['DJANGO_CONFIGURATION'] = 'Testing'
    importer.install()

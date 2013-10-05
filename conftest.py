import django
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# Ignore the Gunicorn configuration.
collect_ignore = ['gunicorn.conf.py']

def pytest_report_header(config):
    return 'django: ' + django.get_version()

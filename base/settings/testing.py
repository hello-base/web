# -*- coding: utf-8 -*-
from configurations import values

from .base import Base as Settings


class Testing(Settings):
    # Debug Settings.
    # --------------------------------------------------------------------------
    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = values.BooleanValue(False)

    # Database Configuration.
    # --------------------------------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    # django-celery.
    # --------------------------------------------------------------------------
    Settings.INSTALLED_APPS += ['kombu.transport.django']
    BROKER_URL = 'django://'

    # django-haystack.
    # --------------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    # Static File Configuration.
    # --------------------------------------------------------------------------
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

    # Media Storage Configuration.
    # --------------------------------------------------------------------------
    # Amazon Web Services
    AWS_STORAGE_BUCKET_NAME = 'test-bucket'

    # ...
    CDN_DOMAIN = 'cdn.example.net'
    MEDIA_URL = 'https://%s/media/' % (CDN_DOMAIN)

    # Authentication Configuration.
    # --------------------------------------------------------------------------
    HELLO_BASE_CLIENT_ID = 'client-id'
    HELLO_BASE_CLIENT_SECRET = 'client-secret'
    OAUTH_AUTHORIZATION_URL = 'https://testserver/oauth/authorize/'
    OAUTH_TOKEN_URL = 'https://testserver/oauth/token/'

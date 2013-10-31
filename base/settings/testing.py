# -*- coding: utf-8 -*-
from .base import Base as Settings


class Testing(Settings):
    # Database Configuration.
    # --------------------------------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test-base',
        }
    }

    # django-celery.
    # --------------------------------------------------------------------------
    Settings.INSTALLED_APPS += ['kombu.transport.django', 'djcelery']
    BROKER_URL = 'django://'

    # django-haystack.
    # --------------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    # Media Storage Configuration.
    # --------------------------------------------------------------------------
    # Amazon Web Services
    AWS_STORAGE_BUCKET_NAME = 'test-bucket'

    # django-s3-folder-storage
    DEFAULT_S3_PATH = 'media'
    STATIC_S3_PATH = 'static'
    CDN_DOMAIN = 'cdn.example.net'
    MEDIA_URL = 'https://%s/%s/' % (CDN_DOMAIN, DEFAULT_S3_PATH)
    STATIC_URL = 'https://%s/%s/' % (CDN_DOMAIN, STATIC_S3_PATH)

    # Authentication Configuration.
    # --------------------------------------------------------------------------
    HELLO_BASE_CLIENT_ID = 'client-id'
    HELLO_BASE_CLIENT_SECRET = 'client-secret'
    OAUTH_AUTHORIZATION_URL = 'https://testserver/oauth/authorize/'
    OAUTH_TOKEN_URL = 'https://testserver/oauth/token/'

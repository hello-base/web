# -*- coding: utf-8 -*-
from configurations import values

from .base import Base as Settings


class Development(Settings):
    MIDDLEWARE_CLASSES = Settings.MIDDLEWARE_CLASSES

    # Installed Applications.
    # --------------------------------------------------------------------------
    INSTALLED_APPS = Settings.INSTALLED_APPS + []

    # Site Configuration.
    # --------------------------------------------------------------------------
    ALLOWED_HOSTS = ['*']

    # Debug Settings.
    # --------------------------------------------------------------------------
    DEBUG = values.BooleanValue(True)

    # Authentication Configuration.
    # --------------------------------------------------------------------------
    MEISHI_ENDPOINT = 'https://localhost:8443/api/'
    OAUTH_AUTHORIZATION_URL = 'https://localhost:8443/authorize/'
    OAUTH_TOKEN_URL = 'https://localhost:8443/token/'
    OAUTH_REDIRECT_URL = 'https://localhost:8444/accounts/authenticated/'

    # django-celery.
    # --------------------------------------------------------------------------
    CELERY_ALWAYS_EAGER = True  # http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True  # http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions

    # django-extensions
    # --------------------------------------------------------------------------
    GRAPH_MODELS = {
        'all_applications': True,
        'group_models': True,
    }

    # django-haystack.
    # --------------------------------------------------------------------------
    ELASTICSEARCH_DEFAULT_ANALYZER = 'snowball'
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'apps.search_backends.KuromojiElastcisearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

    # django-imagekit.
    # --------------------------------------------------------------------------
    IMAGEKIT_CACHEFILE_DIR = 'cache'
    IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
    IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'

    # ...
    # --------------------------------------------------------------------------
    CDN_DOMAIN = 'dxglax8otc2dg.cloudfront.net'
    MEDIA_URL = 'https://%s/media/' % (CDN_DOMAIN)

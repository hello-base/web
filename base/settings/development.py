# -*- coding: utf-8 -*-
import os
import sys

from configurations import values

from .base import Base as Settings


class Development(Settings):
    # Installed Applications.
    # ------------------------------------------------------------------
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'debugtools',
        'django_extensions',
    ]

    # Site Configuration.
    # ------------------------------------------------------------------
    ALLOWED_HOSTS = ['*']

    # Debug Settings.
    # ------------------------------------------------------------------
    DEBUG = values.BooleanValue(True)

    # Authentication Configuration.
    # ------------------------------------------------------------------
    MEISHI_ENDPOINT = 'https://localhost:8443/api/'
    OAUTH_AUTHORIZATION_URL = 'https://localhost:8443/authorize/'
    OAUTH_TOKEN_URL = 'https://localhost:8443/token/'
    OAUTH_REDIRECT_URL = 'https://localhost:8444/accounts/authenticated/'

    # django-celery.
    # ------------------------------------------------------------------
    INSTALLED_APPS += ['kombu.transport.django',]
    BROKER_URL = 'django://'
    CELERY_ALWAYS_EAGER = True  # http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True  # http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

    # django-debugtoolbar.
    # ------------------------------------------------------------------
    INSTALLED_APPS += ['debug_toolbar',]
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES = Settings.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }

    # django-devserver.
    # ------------------------------------------------------------------
    INSTALLED_APPS += ['devserver',]
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.cache.CacheSummaryModule',
    )

    # django-ecstatic / django-staticbuilder
    # ------------------------------------------------------------------
    MIDDLEWARE_CLASSES += ('staticbuilder.middleware.BuildOnRequest',)

    # django-extensions
    # ------------------------------------------------------------------
    GRAPH_MODELS = {
        'all_applications': True,
        'group_models': True,
    }

    # django-haystack.
    # ------------------------------------------------------------------
    ELASTICSEARCH_DEFAULT_ANALYZER = 'snowball'
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'components.search_backends.KuromojiElastcisearchEngine',
            # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

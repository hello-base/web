# -*- coding: utf-8 -*-
from configurations import values

from .base import Base as Settings


class Development(Settings):
    MIDDLEWARE_CLASSES = Settings.MIDDLEWARE_CLASSES

    # Installed Applications.
    # --------------------------------------------------------------------------
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'debugtools',
        'django_extensions',
    ]

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

    # django-debugtoolbar.
    # --------------------------------------------------------------------------
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    # django-devserver.
    # --------------------------------------------------------------------------
    INSTALLED_APPS += ['devserver']
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.cache.CacheSummaryModule',
    )

    # django-ecstatic / django-staticbuilder
    # --------------------------------------------------------------------------
    MIDDLEWARE_CLASSES += ('staticbuilder.middleware.BuildOnRequest',)

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
            'ENGINE': 'components.search_backends.KuromojiElastcisearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

    # django-imagekit.
    # --------------------------------------------------------------------------
    IMAGEKIT_CACHEFILE_DIR = 'cache'
    IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
    IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'

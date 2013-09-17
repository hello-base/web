import os
import sys

from .base import Base as Settings


class Development(Settings):
    # Default / Debug Settings
    DEBUG = True
    INTERNAL_IPS = ('127.0.0.1',)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Database / Caching
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    # Middleware
    MIDDLEWARE_CLASSES = (
        'django.middleware.gzip.GZipMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Installed Applications
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'debug_toolbar',
        'debugtools',
        'devserver',
        'django_extensions',
    ]

    # Secret Key
    SECRET_KEY = '@5zyl)e#a#xmgzg*_%7=$m#kbvc%mi%j-+b(13yaml!dre7l!u'

    # Static Media Settings
    STATIC_ROOT = ''
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.normpath(os.path.join(Settings.SITE_ROOT, 'static')),
    )

    # Sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    SESSION_COOKIE_SECURE = False

    # Django Authentication (OAuth, etc.)
    MEISHI_ENDPOINT = 'https://localhost:8443/api/'
    OAUTH_AUTHORIZATION_URL = 'https://localhost:8443/authorize/'
    OAUTH_TOKEN_URL = 'https://localhost:8443/token/'
    OAUTH_REDIRECT_URL = 'https://localhost:8444/accounts/authenticated/'

    # Django DevServer
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.cache.CacheSummaryModule',
    )

    # Django Haystack
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

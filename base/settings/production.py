# -*- coding: utf-8 -*-
import os
import sys

from configurations import values
from redisify import redisify

from .base import Base as Settings


class Production(Settings):
    # Installed Applications (featuring Production).
    # ------------------------------------------------------------------
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'gunicorn',
        'raven.contrib.django',
    ]

    # Middleware Configuration.
    # ------------------------------------------------------------------
    MIDDLEWARE_CLASSES = (
        'django.middleware.gzip.GZipMiddleware',
        'django.middleware.common.CommonMiddleware',
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Debug Settings.
    # ------------------------------------------------------------------
    DEBUG = values.BooleanValue(False)

    # Secret Key Configuration.
    # ------------------------------------------------------------------
    SECRET_KEY = os.environ.get('SECUREKEY_VIOLET_KEY', '').split(',')[0]

    # Caching Configuration.
    # ------------------------------------------------------------------
    CACHES = redisify(default='redis://localhost')

    # Separate the staticfiles cache from the normal Redis cache.
    CACHES['staticfiles'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
        # Long cache timeout for staticfiles, since this is used
        # heavily by the optimizing storage.
        'TIMEOUT': 60 * 60 * 24 * 365,
    }

    # django-secure.
    # ------------------------------------------------------------------
    INSTALLED_APPS += ['djangosecure',]
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)

    # Site Configuration.
    # ------------------------------------------------------------------
    ALLOWED_HOSTS = ['.hello-base.com', '.hello-base.com.',]

    # Media Storage Configuration.
    # ------------------------------------------------------------------
    INSTALLED_APPS += [
        's3_folder_storage',
        'storages',
    ]
    DEFAULT_FILE_STORAGE = 'components.storage.MediaFilesStorage'
    STATICFILES_STORAGE = 'components.storage.S3ManifestStorage'

    # Amazon Web Services
    AWS_ACCESS_KEY_ID = values.SecretValue(environ_prefix='', environ_name='AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = values.SecretValue(environ_prefix='', environ_name='AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = values.SecretValue(environ_prefix='', environ_name='AWS_STORAGE_BUCKET_NAME')
    AWS_AUTO_CREATE_BUCKET = True
    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = False
    AWS_IS_GZIPPED = False

    # AWS Caching Settings
    AWS_EXPIRY = 60 * 60 * 24 * 7
    AWS_HEADERS = {'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY)}

    # django-s3-folder-storage
    DEFAULT_S3_PATH = 'media'
    STATIC_S3_PATH = 'static'
    CDN_DOMAIN = 'hellobase-revyverinc.netdna-ssl.com'
    MEDIA_URL = '//%s/%s/' % (CDN_DOMAIN, DEFAULT_S3_PATH)
    STATIC_URL = '//%s/%s/' % (CDN_DOMAIN, STATIC_S3_PATH)

    # Template Configuration.
    # ------------------------------------------------------------------
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    # Authentication Configuration.
    # ------------------------------------------------------------------
    MEISHI_ENDPOINT = 'https://id.hello-base.com/api/'
    OAUTH_AUTHORIZATION_URL = 'https://id.hello-base.com/oauth/authorize/'
    OAUTH_TOKEN_URL = 'https://id.hello-base.com/oauth/token/'
    OAUTH_REDIRECT_URL = 'https://hello-base.com/accounts/authenticated/'

    # Logging Configuration.
    # ------------------------------------------------------------------
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stdout
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.handlers.SentryHandler',
                'filters': ['require_debug_false'],
            },
        },
        'loggers': {
            # This is a "catch all" logger.
            '': {
                'level': 'DEBUG',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'boto': {
                'level': 'WARNING',
                'handlers': ['sentry'],
                'propagate': False,
            },
        }
    }

    # django-haystack (ElasticSearch).
    # ------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': os.environ.get('BONSAI_URL', ''),
            'INDEX_NAME': 'haystack',
        },
    }

    # django-ecstatic / django-staticbuilder
    # ------------------------------------------------------------------
    ECSTATIC_MANIFEST_CACHE = 'staticfiles'

    # django-imagekit.
    # ------------------------------------------------------------------
    IMAGEKIT_CACHEFILE_DIR = 'cache'
    IMAGEKIT_CACHE_BACKEND = 'staticfiles'
    IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
    IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'
    # IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Async'

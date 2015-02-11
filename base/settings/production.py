# -*- coding: utf-8 -*-
import os
import sys

from celery.schedules import crontab
from configurations import values
from postgresify import postgresify
from redisify import redisify

from .base import Base as Settings


class Production(Settings):
    # Installed Applications (featuring Production).
    # --------------------------------------------------------------------------
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'raven.contrib.django',
    ]

    # Middleware Configuration.
    # --------------------------------------------------------------------------
    MIDDLEWARE_CLASSES = (
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    )

    # Debug Settings.
    # --------------------------------------------------------------------------
    DEBUG = values.BooleanValue(True)

    # Secret Key Configuration.
    # --------------------------------------------------------------------------
    SECRET_KEY = os.environ.get('SECUREKEY_VIOLET_KEY', '').split(',')[0]

    # Database Configuration.
    # --------------------------------------------------------------------------
    DATABASES = postgresify()
    if 'default' in DATABASES:  # pragma: no branch
        DATABASES['default']['CONN_MAX_AGE'] = 600

    # Caching Configuration.
    # --------------------------------------------------------------------------
    CACHES = redisify(default='redis://localhost')
    CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

    # Separate the staticfiles cache from the normal Redis cache.
    CACHES['staticfiles'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
        # Long cache timeout for staticfiles, since this is used
        # heavily by the optimizing storage.
        'TIMEOUT': 60 * 60 * 24 * 365,
    }

    # django-secure.
    # --------------------------------------------------------------------------
    INSTALLED_APPS += ['djangosecure']
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(False)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_REDIRECT_EXEMPT = [r'https?://(blog\.hello-base\.com\/?)']

    # Site Configuration.
    # --------------------------------------------------------------------------
    ALLOWED_HOSTS = ['.hello-base.com', '.hello-base.com.']

    # Media Storage Configuration.
    # --------------------------------------------------------------------------
    INSTALLED_APPS += [
        's3_folder_storage',
        'storages',
    ]
    DEFAULT_FILE_STORAGE = 'base.apps.storage.MediaFilesStorage'
    STATICFILES_STORAGE = 'base.apps.storage.S3ManifestStorage'

    # Amazon Web Services
    AWS_ACCESS_KEY_ID = values.SecretValue(environ_prefix='')
    AWS_SECRET_ACCESS_KEY = values.SecretValue(environ_prefix='')
    AWS_STORAGE_BUCKET_NAME = values.SecretValue(environ_prefix='')
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
    CDN_DOMAIN = 'dxglax8otc2dg.cloudfront.net'
    MEDIA_URL = 'https://%s/%s/' % (CDN_DOMAIN, DEFAULT_S3_PATH)
    STATIC_URL = 'https://%s/%s/' % (CDN_DOMAIN, STATIC_S3_PATH)

    # Template Configuration.
    # --------------------------------------------------------------------------
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    # Authentication Configuration.
    # --------------------------------------------------------------------------
    MEISHI_ENDPOINT = 'https://id.hello-base.com/api/'
    OAUTH_AUTHORIZATION_URL = 'https://id.hello-base.com/oauth/authorize/?approval_prompt=auto'
    OAUTH_TOKEN_URL = 'https://id.hello-base.com/oauth/token/'
    OAUTH_REDIRECT_URL = 'https://hello-base.com/accounts/authenticated/'

    # Logging Configuration.
    # --------------------------------------------------------------------------
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

    # django-celery.
    # --------------------------------------------------------------------------
    BROKER_URL = values.Value(environ_prefix='', environ_name='OPENREDIS_URL')
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_TIMEZONE = 'Asia/Tokyo'
    CELERYBEAT_SCHEDULE = {
        'fetch_latest_youtube_videos': {
            'task': 'tasks.fetch_latest_videos',
            'schedule': crontab(minute=0, hour=0),
        },
    }

    # django-haystack (ElasticSearch).
    # --------------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'base.apps.search_backends.KuromojiElastcisearchEngine',
            'URL': os.environ.get('BONSAI_URL', ''),
            'INDEX_NAME': 'haystack',
        },
    }

    # django-ecstatic / django-staticbuilder
    # --------------------------------------------------------------------------
    ECSTATIC_MANIFEST_CACHE = 'staticfiles'
    STATICBUILDER_BUILD_COMMANDS = ['inv compile']

    # django-imagekit.
    # --------------------------------------------------------------------------
    IMAGEKIT_CACHE_BACKEND = 'staticfiles'
    IMAGEKIT_CACHEFILE_DIR = 'cache'
    IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
    IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'

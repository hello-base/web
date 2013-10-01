import os
import sys

from configurations import values
from redisify import redisify

from .base import Base as Settings


class Production(Settings):
    # Default / Debug Settings
    DEBUG = False
    ALLOWED_HOSTS = ['.hello-base.com', '.hello-base.com.',]

    # Template Settings
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    # Middleware
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

    # Installed Applications
    INSTALLED_APPS = Settings.INSTALLED_APPS + [
        'djangosecure',
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stdout
            },
        },
        'loggers': {
            'analytics': {
                'level': 'DEBUG',
                'handlers': ['console', 'sentry'],
                'propagate': True,
            },
            'django': {
                'level': 'INFO',
                'handlers': ['console', 'sentry'],
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'django.request': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'oauthlib': {
                'level': 'DEBUG',
                'handlers': ['sentry'],
                'propagate': True,
            },
        },
    }

    # File / Media / Static Media Settings
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '//%s.s3.amazonaws.com/media/' % Settings.AWS_STORAGE_BUCKET_NAME
    STATIC_S3_PATH = 'static'
    STATIC_ROOT = '/%s/' % STATIC_S3_PATH
    STATIC_URL = '//%s.s3.amazonaws.com/static/' % Settings.AWS_STORAGE_BUCKET_NAME
    STATICFILES_DIRS = (
        os.path.normpath(os.path.join(Settings.SITE_ROOT, 'static')),
    )
    STATICFILES_STORAGE = 'components.storage.S3PipelineStorage'

    # Django Authentication (OAuth, etc.)
    OAUTH_AUTHORIZATION_URL = 'https://id.hello-base.com/authorize/'
    OAUTH_TOKEN_URL = 'https://id.hello-base.com/token/'
    OAUTH_REDIRECT_URL = 'https://hello-base.com/accounts/authenticated/'

    # Django Secure
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_FRAME_DENY = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    # Secret Key
    SECRET_KEY = os.environ.get('SECUREKEY_VIOLET_KEY', '').split(',')[0]

    # Heroku ===========================================================
    # Django Haystack (ElasticSearch)
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': os.environ.get('BONSAI_URL', ''),
            'INDEX_NAME': 'haystack',
        },
    }

    # OpenRedis
    CACHES = redisify(default='redis://localhost')
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_URL = os.environ.get('OPENREDIS_URL', '')

    # Sentry
    if 'SENTRY_DSN' in os.environ:
        # Add raven to the list of installed apps
        INSTALLED_APPS = Settings.INSTALLED_APPS + ['raven.contrib.django', ]

    # Further StaticFiles Nonsense
    # Separate the staticfiles cache from the normal Redis cache.
    CACHES['staticfiles'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
        # Long cache timeout for staticfiles, since this is used
        # heavily by the optimizing storage.
        'TIMEOUT': 60 * 60 * 24 * 365,
    }

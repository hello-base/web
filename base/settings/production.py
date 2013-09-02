import os
import sys

from .base import Base as Settings


class Production(Settings):
    DEBUG = True

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    # # Middleware
    # MIDDLEWARE_CLASSES = (
    #     'django.middleware.gzip.GZipMiddleware',
    #     'djangosecure.middleware.SecurityMiddleware',
    #     'django.middleware.common.CommonMiddleware',
    #     'django.contrib.sessions.middleware.SessionMiddleware',
    #     'django.middleware.csrf.CsrfViewMiddleware',
    #     'django.contrib.auth.middleware.AuthenticationMiddleware',
    #     'django.contrib.messages.middleware.MessageMiddleware',
    #     'social_auth.middleware.SocialAuthExceptionMiddleware',
    #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #     'django_hosts.middleware.HostsMiddleware',
    # )

    # # Installed Applications
    # INSTALLED_APPS = Settings.INSTALLED_APPS + [
    #     'djangosecure',
    # ]

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'analytics': {
                'handlers': ['console', 'sentry'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django': {
                'level': 'INFO',
                'handlers': ['sentry'],
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['sentry'],
                'propagate': False,
            },
            'django.request': {
                'level': 'ERROR',
                'handlers': ['sentry'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['sentry'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['sentry'],
                'propagate': False,
            },
        },
    }

    # File / Media / Static Media Settings
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'meishi/media'
    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '//%s.s3.amazonaws.com/base/media/' % Settings.AWS_STORAGE_BUCKET_NAME
    STATIC_S3_PATH = 'meishi/static'
    STATIC_ROOT = '/%s/' % STATIC_S3_PATH
    STATIC_URL = '//%s.s3.amazonaws.com/base/static/' % Settings.AWS_STORAGE_BUCKET_NAME
    STATICFILES_DIRS = (
        os.path.normpath(os.path.join(Settings.SITE_ROOT, 'static')),
    )
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'

    # # Django Secure
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_FRAME_DENY = True
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_SECONDS = 1800
    # SECURE_SSL_REDIRECT = True
    # SESSION_COOKIE_SECURE = True

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

    # Sentry
    if 'SENTRY_DSN' in os.environ:
        # Add raven to the list of installed apps
        INSTALLED_APPS = Settings.INSTALLED_APPS + ['raven.contrib.django', ]

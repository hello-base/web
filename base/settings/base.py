import datetime
import os

from os.path import abspath, basename, dirname, join, normpath
from sys import path

from configurations import Settings
from dj_database_url import config as database_config


class Base(Settings):
    # Path Configuration
    DJANGO_ROOT = dirname(dirname(abspath(__file__)))
    SITE_ROOT = dirname(DJANGO_ROOT)
    SITE_NAME = basename(DJANGO_ROOT)

    # Add our project to our pythonpath, this way we don't need to type our
    # project name in our dotted import paths:
    path.append(DJANGO_ROOT)

    # Default / Debug Settings
    ROOT_URLCONF = '%s.urls' % SITE_NAME
    SITE_ID = 1
    TEMPLATE_DEBUG = Settings.DEBUG

    # Emails
    ADMINS = [('Bryan Veloso', 'bryan@hello-ranking.com')]
    MANAGERS = [('Jennifer Verduzco', 'jen@hello-ranking.com')]

    # Localization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Database / Caching
    DATABASES = {'default': database_config(default='postgres://localhost')}

    # Template Settings
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
    )
    TEMPLATE_DIRS = (normpath(join(DJANGO_ROOT, 'templates')),)
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # Middleware
    MIDDLEWARE_CLASSES = (
        'django.middleware.gzip.GZipMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Installed Applications
    DJANGO_APPLICATIONS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
    ]
    COMPONENTS = [
        'components.events',
        'components.goods',
        'components.people',
        'components.releases',
        'components.releases.music',
    ]
    PLUGINS = [
        'gunicorn',
        'south',
    ]
    ADMINISTRATION = [
        'django.contrib.admin',
    ]
    INSTALLED_APPS = DJANGO_APPLICATIONS + COMPONENTS + PLUGINS + ADMINISTRATION

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

    # Sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

    # Media Settings
    MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
    MEDIA_URL = '/media/'
    MEDIA_STORAGE_BUCKET_NAME = 'hello-ranking-media'

    # Static Media Settings
    STATIC_ROOT = normpath(join(SITE_ROOT, 'static'))
    STATIC_URL = '/static/'
    STATICFILES_DIRS = ()
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    STATIC_STORAGE_BUCKET_NAME = 'hello-ranking-static'

    # Django Storages
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_HEADERS = {
        'Expires': (datetime.date.today() + datetime.timedelta(days=365)).strftime('%a, %d %b %Y 20:00:00 GMT'),
        'Cache-Control': 'max-age=31536000, private'
    }
    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = False
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = MEDIA_STORAGE_BUCKET_NAME
    AWS_STATIC_STORAGE_BUCKET_NAME = STATIC_STORAGE_BUCKET_NAME

    # South
    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}

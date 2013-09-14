import datetime
import os

from os.path import abspath, basename, dirname, join, normpath
from sys import path

from configurations import Configuration, values
from postgresify import postgresify


class Base(Configuration):
    # Path Configuration
    DJANGO_ROOT = dirname(dirname(abspath(__file__)))
    SITE_ROOT = dirname(DJANGO_ROOT)
    SITE_NAME = basename(DJANGO_ROOT)

    # Add our project to our pythonpath, this way we don't need to type our
    # project name in our dotted import paths:
    path.append(DJANGO_ROOT)

    # Default / Debug Settings
    ALLOWED_HOSTS = []
    DATE_FORMAT = 'Y/m/d'
    DEBUG = True
    ROOT_URLCONF = '%s.urls' % SITE_NAME
    SITE_ID = 1
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)
    WSGI_APPLICATION = 'wsgi.application'

    # Emails
    ADMINS = [('Bryan Veloso', 'bryan@hello-base.com')]
    MANAGERS = [('Jennifer Verduzco', 'jen@hello-base.com')]

    # Localization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Database / Caching
    DATABASES = postgresify()

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
        'components.merchandise',
        'components.merchandise.goods',
        'components.merchandise.music',
        'components.people',
    ]
    PLUGINS = [
        'floppyforms',
        'gunicorn',
        'haystack',
        's3_folder_storage',
        'south',
        'storages',
        'typogrify',
    ]
    ADMINISTRATION = [
        'django.contrib.admin',
    ]
    INSTALLED_APPS = DJANGO_APPLICATIONS + COMPONENTS + PLUGINS + ADMINISTRATION

    # Sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

    # File / Media / Static Media Settings
    MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
    MEDIA_URL = '/media/'
    STATIC_ROOT = normpath(join(SITE_ROOT, 'static'))
    STATIC_URL = '/static/'

    # Django Haystack
    HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

    # Django Storages
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_HEADERS = {
        'Expires': (datetime.date.today() + datetime.timedelta(days=365)).strftime('%a, %d %b %Y 20:00:00 GMT'),
        'Cache-Control': 'max-age=31536000, private'
    }
    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = False
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = 'hello-base'

    # South
    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}

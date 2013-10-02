# -*- coding: utf-8 -*-
import datetime
import os

from os.path import abspath, basename, dirname, join, normpath
from sys import path

from django.core.urlresolvers import reverse_lazy

from configurations import Configuration, values
from postgresify import postgresify


class Base(Configuration):
    # Path Configuration.
    # ------------------------------------------------------------------
    DJANGO_ROOT = dirname(dirname(abspath(__file__)))
    SITE_ROOT = dirname(DJANGO_ROOT)
    SITE_NAME = basename(DJANGO_ROOT)

    # Add our project to our pythonpath, this way we don't need to
    # type our project name in our dotted import paths:
    path.append(DJANGO_ROOT)

    # Installed Applications.
    # ------------------------------------------------------------------
    DJANGO = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.sitemaps',
        'django.contrib.sites',
        'django.contrib.staticfiles',
    ]
    COMPONENTS = [
        'components.accounts',
        'components.events',
        'components.merchandise',
        'components.merchandise.goods',
        'components.merchandise.music',
        'components.people',
    ]
    PLUGINS = [
        'floppyforms',
        'haystack',
        'imagekit',
        'south',
        'typogrify',
    ]
    ADMINISTRATION = [
        'grappelli',
        'django.contrib.admin',
    ]
    INSTALLED_APPS = DJANGO + COMPONENTS + PLUGINS + ADMINISTRATION

    # Middleware Configuration.
    # ------------------------------------------------------------------
    MIDDLEWARE_CLASSES = (
        'django.middleware.gzip.GZipMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Debug Settings.
    # ------------------------------------------------------------------
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    # Secret Key Configuration.
    # ------------------------------------------------------------------
    SECRET_KEY = '@5zyl)e#a#xmgzg*_%7=$m#kbvc%mi%j-+b(13yaml!dre7l!u'

    # Manager Configuration.
    # ------------------------------------------------------------------
    ADMINS = [('Bryan Veloso', 'bryan@hello-base.com')]
    MANAGERS = [('Jennifer Verduzco', 'jen@hello-base.com')]

    # Database Configuration.
    # ------------------------------------------------------------------
    DATABASES = postgresify()

    # Caching Configuration.
    # ------------------------------------------------------------------
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }

    # General Configuration.
    # ------------------------------------------------------------------
    LANGUAGE_CODE = 'en-us'
    SITE_ID = 1
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Template Configuration.
    # ------------------------------------------------------------------
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

    # Static File Configuration.
    # ------------------------------------------------------------------
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        normpath(join(DJANGO_ROOT, 'static')),
    )
    STATICFILES_FINDERS = (
        'staticbuilder.finders.BuiltFileFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media Configuration.
    # ------------------------------------------------------------------
    MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))
    MEDIA_URL = '/media/'

    # URL Configuration.
    # ------------------------------------------------------------------
    ROOT_URLCONF = '%s.urls' % SITE_NAME
    WSGI_APPLICATION = 'wsgi.application'

    # Authentication Configuration.
    # ------------------------------------------------------------------
    AUTHENTICATION_BACKENDS = (
        'components.accounts.backends.HelloBaseIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
    HELLO_BASE_CLIENT_ID = values.Value('',  environ_prefix=None)
    HELLO_BASE_CLIENT_SECRET = values.Value('',  environ_prefix=None)
    LOGIN_URL = reverse_lazy('oauth-authorize')
    # LOGOUT_URL = 'oauth-deauthorize'

    # Custom User Application Defaults.
    # ------------------------------------------------------------------
    AUTH_USER_MODEL = 'accounts.editor'

    # Logging Configuration.
    # ------------------------------------------------------------------
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    # django-ecstatic / django-staticbuilder
    # ------------------------------------------------------------------
    INSTALLED_APPS += [
        'ecstatic',
        'staticbuilder',
    ]
    ECSTATIC_MANIFEST_FILE = join(DJANGO_ROOT, 'settings', 'manifest.json')
    STATICBUILDER_BUILD_ROOT = join(DJANGO_ROOT, 'build')
    STATICBUILDER_BUILD_COMMANDS = ['inv yuglify']

    # django-grappelli.
    # ------------------------------------------------------------------
    GRAPPELLI_ADMIN_TITLE = 'Hello! Base Administration'

    # django-haystack.
    # ------------------------------------------------------------------
    HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

    # South.
    # ------------------------------------------------------------------
    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}

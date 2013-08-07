import os
import sys

from .base import Base as Settings


class Production(Settings):
    DEBUG = True

    # TEMPLATE_LOADERS = (
    #     ('django.template.loaders.cached.Loader', (
    #         'django.template.loaders.filesystem.Loader',
    #         'django.template.loaders.app_directories.Loader',
    #     )),
    # )

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
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'strm': sys.stdout
            },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

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

    # Heroku =================================================================
    # Sentry
    if 'SENTRY_DSN' in os.environ:
        # Add raven to the list of installed apps
        INSTALLED_APPS = Settings.INSTALLED_APPS + ['raven.contrib.django', ]

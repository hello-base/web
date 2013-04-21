import os
import sys

from .base import Base as Settings


class Development(Settings):
    # Default / Debug Settings
    DEBUG = True
    INTERNAL_IPS = ('127.0.0.1',)
    TEMPLATE_STRING_IF_INVALID = 'INVALID EXPRESSION: %s'

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

    # Django DevServer
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.cache.CacheSummaryModule',
    )

    # Django Tastypie
    TASTYPIE_FULL_DEBUG = True

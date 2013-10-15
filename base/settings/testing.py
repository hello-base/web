# -*- coding: utf-8 -*-
import os

from .base import Base as Settings


class Testing(Settings):
    # Installed Applications.
    # ------------------------------------------------------------------
    INSTALLED_APPS = [
        'components.accounts',
        'components.events',
        'components.merchandise',
        'components.merchandise.goods',
        'components.merchandise.media',
        'components.merchandise.music',
        'components.people',
    ]

    # Database Configuration.
    # ------------------------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test-base',
        }
    }

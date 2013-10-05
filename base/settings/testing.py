# -*- coding: utf-8 -*-
import os

from .base import Base as Settings


class Testing(Settings):
    # Database Configuration.
    # ------------------------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }

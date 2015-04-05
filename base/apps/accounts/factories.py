# -*- coding: utf-8 -*-
import datetime
import factory

from . import models


class EditorFactory(factory.DjangoModelFactory):
    base_id = factory.Sequence(lambda i: '%d' % i)
    username = factory.Sequence(lambda i: 'dancer#%s' % i)
    password = 'dancefloor'
    name = 'Tsunku'
    email = factory.LazyAttribute(lambda a: '{0}@example.com'.format(a.username).lower())
    started = datetime.datetime.now()

    class Meta:
        model = models.Editor

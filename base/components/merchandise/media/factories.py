# -*- coding: utf-8 -*-
import datetime
import factory

from django.template.defaultfilters import slugify

from components.merchandise.factories import MerchandiseFactory

from . import models


class VideodiscFactory(MerchandiseFactory):
    FACTORY_FOR = models.Videodisc

    romanized_name = factory.Sequence(lambda i: 'videodisc#%s' % i)
    name = factory.Sequence(lambda i: 'videodisc#%s' % i)
    kind = 1  # (1, 'bestshot', 'Best Shot')
    slug = factory.LazyAttribute(lambda s: slugify(s.romanized_name))


class VideodiscFormatFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.VideodiscFormat

    parent = factory.SubFactory(VideodiscFactory)
    kind = 1  # (1, 'dvd', 'DVD')
    released = factory.LazyAttribute(lambda d: datetime.datetime.utcnow())
    catalog_number = 'TEST-0000'


class ClipFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Clip

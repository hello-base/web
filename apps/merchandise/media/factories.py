# -*- coding: utf-8 -*-
import datetime
import factory

from django.template.defaultfilters import slugify

from apps.merchandise.factories import MerchandiseFactory

from . import models


class VideodiscFactory(MerchandiseFactory):
    kind = 1  # (1, 'bestshot', 'Best Shot')
    slug = factory.LazyAttribute(lambda s: slugify(s.romanized_name))

    class Meta:
        model = models.Videodisc


class VideodiscFormatFactory(factory.django.DjangoModelFactory):
    parent = factory.SubFactory(VideodiscFactory)
    kind = 1  # (1, 'dvd', 'DVD')
    released = factory.LazyAttribute(lambda d: datetime.datetime.utcnow())
    catalog_number = 'TEST-0000'

    class Meta:
        model = models.VideodiscFormat


class ClipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Clip

# -*- coding: utf-8 -*-
import datetime
import factory
import uuid

from . import models


class MerchandiseFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'merchandise#%s' % i)
    name = factory.Sequence(lambda i: 'merchandise#%s' % i)
    released = factory.LazyAttribute(lambda d: datetime.datetime.utcnow())
    price = 500
    uuid = uuid.uuid4()

    class Meta:
        model = models.Merchandise
        abstract = True

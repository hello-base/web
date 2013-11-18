# -*- coding: utf-8 -*-
import factory

from . import models


class CorrelationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Correlation

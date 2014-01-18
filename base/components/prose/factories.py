# -*- coding: utf-8 -*-
import factory

from . import models


class FactFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Fact

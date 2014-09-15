# -*- coding: utf-8 -*-
import factory

from . import models


class ShopFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Shop


class GoodFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Good

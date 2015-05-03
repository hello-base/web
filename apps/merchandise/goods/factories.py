# -*- coding: utf-8 -*-
import factory

from . import models


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Shop


class GoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Good

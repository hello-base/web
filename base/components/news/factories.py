# -*- coding: utf-8 -*-
import factory

from . import models


class ItemFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Item


class ItemImageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.ItemImage


class UpdateFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Update

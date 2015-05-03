# -*- coding: utf-8 -*-
import factory

from . import models


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Item


class ItemImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ItemImage


class UpdateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Update

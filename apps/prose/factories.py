# -*- coding: utf-8 -*-
import factory

from . import models


class FactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Fact


class SummaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Summary

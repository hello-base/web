# -*- coding: utf-8 -*-
import factory

from . import models


class ShowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Show


class TimeSlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TimeSlot


class EpisodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Episode


class MagazineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Magazine


class IssueFactory(factory.django.DjangoModelFactory):
    magazine = factory.SubFactory(MagazineFactory)

    class Meta:
        model = models.Issue


class IssueImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.IssueImage


class CardSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CardSet


class CardFactory(factory.django.DjangoModelFactory):
    issue = factory.SubFactory(IssueFactory)

    class Meta:
        model = models.Card

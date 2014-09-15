# -*- coding: utf-8 -*-
import factory

from . import models


class ShowFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Show


class TimeSlotFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.TimeSlot


class EpisodeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Episode


class MagazineFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Magazine


class IssueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Issue

    magazine = factory.SubFactory(MagazineFactory)


class IssueImageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.IssueImage


class CardSetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.CardSet


class CardFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Card

    issue = factory.SubFactory(IssueFactory)

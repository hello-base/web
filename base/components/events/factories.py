import datetime
import factory

from . import models


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Event


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Performance


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Venue

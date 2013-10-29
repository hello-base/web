import datetime
import factory

from . import models


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Event

    romanized_name = factory.Sequence(lambda i: 'event#%s' % i)


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Performance

    day = datetime.date.today()
    event = factory.SubFactory(EventFactory)
    romanized_name = factory.Sequence(lambda i: 'performance#%s' % i)


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Venue

    romanized_name = factory.Sequence(lambda i: 'venue#%s' % i)

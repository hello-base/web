import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Event

    romanized_name = factory.Sequence(lambda i: 'event#%s' % i)
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Performance

    day = datetime.date.today()
    event = factory.SubFactory(EventFactory)
    romanized_name = factory.Sequence(lambda i: 'performance#%s' % i)


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Venue

    romanized_name = factory.Sequence(lambda i: 'venue#%s' % i)
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))

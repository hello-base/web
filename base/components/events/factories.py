import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Event

    romanized_name = factory.Sequence(lambda i: 'event#%s' % i)
    name = factory.Sequence(lambda i: 'event#%s' % i)
    nickname = factory.Sequence(lambda i: 'nickname#%s' % i)
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))


class ActivityFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Activity

    day = datetime.date.today()
    event = factory.SubFactory(EventFactory)
    romanized_name = factory.Sequence(lambda i: 'activity#%s' % i)


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Venue

    romanized_name = factory.Sequence(lambda i: 'venue#%s' % i)
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))

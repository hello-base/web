import datetime
import factory

from components.people.factories import GroupFactory

from . import models


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.History

    datetime = factory.LazyAttribute(lambda x: datetime.datetime.now())
    source_object = factory.SubFactory(GroupFactory)

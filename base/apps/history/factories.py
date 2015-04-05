import datetime
import factory

from base.apps.people.factories import GroupFactory

from . import models


class HistoryFactory(factory.DjangoModelFactory):
    tag = 'test-group-metric'
    datetime = factory.LazyAttribute(lambda x: datetime.datetime.now())
    source_object = factory.SubFactory(GroupFactory)

    class Meta:
        model = models.History

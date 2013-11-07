import factory

from . import models


class HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.History

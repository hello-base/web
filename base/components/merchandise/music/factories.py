import datetime
import factory

from . import models


class BaseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Base
    FACTORY_DJANGO_GET_OR_CREATE = ('romanized_name',)
    ABSTRACT_FACTORY = True


class AlbumFactory(BaseFactory):
    FACTORY_FOR = models.Album

    romanized_name = factory.Sequence(lambda i: 'album#%s' % i)
    released = datetime.datetime.now()


class SingleFactory(BaseFactory):
    FACTORY_FOR = models.Single

    romanized_name = factory.Sequence(lambda i: 'single#%s' % i)
    released = datetime.datetime.now()

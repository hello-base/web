import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class BaseFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Base
    FACTORY_DJANGO_GET_OR_CREATE = ('romanized_name',)
    ABSTRACT_FACTORY = True


class AlbumFactory(BaseFactory):
    FACTORY_FOR = models.Album

    romanized_name = factory.Sequence(lambda i: 'album#%s' % i)
    released = datetime.date.today()
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))


class SingleFactory(BaseFactory):
    FACTORY_FOR = models.Single

    romanized_name = factory.Sequence(lambda i: 'single#%s' % i)
    released = datetime.date.today()
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))


class EditionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Edition

    romanized_name = factory.Sequence(lambda i: 'edition#%s' % i)


class TrackFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Track
    FACTORY_DJANGO_GET_OR_CREATE = ('romanized_name',)

    romanized_name = factory.Sequence(lambda i: 'track#%s' % i)


class VideoFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Video
    FACTORY_DJANGO_GET_OR_CREATE = ('romanized_name',)

    romanized_name = factory.Sequence(lambda i: 'video#%s' % i)

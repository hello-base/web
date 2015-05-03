import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class BaseFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'release#%s' % i)
    released = datetime.date.today()
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))

    class Meta:
        model = models.Base
        abstract = True
        django_get_or_create = ('romanized_name',)


class AlbumFactory(BaseFactory):
    class Meta:
        model = models.Album


class SingleFactory(BaseFactory):
    class Meta:
        model = models.Single


class EditionFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'edition#%s' % i)

    class Meta:
        model = models.Edition


class TrackFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'track#%s' % i)

    class Meta:
        model = models.Track
        django_get_or_create = ('romanized_name',)


class TrackOrderFactory(factory.django.DjangoModelFactory):
    track = factory.SubFactory(TrackFactory)
    edition = factory.SubFactory(EditionFactory)

    class Meta:
        model = models.TrackOrder


class VideoFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'video#%s' % i)

    class Meta:
        model = models.Video
        django_get_or_create = ('romanized_name',)

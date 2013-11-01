import factory

from . import models


class ChannelFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Channel


class VideoFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Video

    channel = factory.SubFactory(ChannelFactory)


class ThumbnailFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Thumbnail

    video = factory.SubFactory(VideoFactory)

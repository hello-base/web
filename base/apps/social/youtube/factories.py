import factory

from . import models


class ChannelFactory(factory.django.DjangoModelFactory):
    username = 'revyver'
    ytid = 'UCZEFNpu29g_QBqkNC619tEA'

    class Meta:
        model = models.Channel


class VideoFactory(factory.django.DjangoModelFactory):
    channel = factory.SubFactory(ChannelFactory)

    class Meta:
        model = models.Video


class ThumbnailFactory(factory.django.DjangoModelFactory):
    video = factory.SubFactory(VideoFactory)

    class Meta:
        model = models.Thumbnail

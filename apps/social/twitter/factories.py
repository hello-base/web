import factory

from . import models


class TwitterUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TwitterUser

class TweetFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(TwitterUserFactory)

    class Meta:
        model = models.Tweet

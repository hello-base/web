import datetime
import factory

from . import models


class TwitterUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.TwitterUser


class TweetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Tweet

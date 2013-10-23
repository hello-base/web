import datetime
import factory

from . import models


class TwitterUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.TwitterUser
    ABSTRACT_FACTORY = True


class TweetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Tweet

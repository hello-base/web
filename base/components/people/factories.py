import datetime
import factory

from . import models


class PersonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Person
    FACTORY_DJANGO_GET_OR_CREATE = ('romanized_name',)
    ABSTRACT_FACTORY = True


class IdolFactory(PersonFactory):
    FACTORY_FOR = models.Idol


class StaffFactory(PersonFactory):
    FACTORY_FOR = models.Staff


class GroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Group

    romanized_name = factory.Sequence(lambda i: 'group#%s' % i)
    started = datetime.datetime.now()


class MembershipFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Membership

    idol = factory.SubFactory(IdolFactory)
    group = factory.SubFactory(GroupFactory)

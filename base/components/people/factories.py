import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class PersonFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Person
    ABSTRACT_FACTORY = True

    romanized_family_name = factory.Sequence(lambda i: 'family#%s' % i)
    romanized_given_name = factory.Sequence(lambda i: 'given#%s' % i)
    romanized_name = factory.LazyAttribute(lambda f: '%s %s' % (f.romanized_family_name, f.romanized_given_name))
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))


class IdolFactory(PersonFactory):
    FACTORY_FOR = models.Idol

    birthdate = datetime.date.today() - datetime.timedelta(days=365 * 18)


class StaffFactory(PersonFactory):
    FACTORY_FOR = models.Staff


class GroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Group

    romanized_name = factory.Sequence(lambda i: 'group#%s' % i)
    slug = factory.LazyAttribute(lambda s: slugify(s.romanized_name))

    started = datetime.date.today() - datetime.timedelta(days=365)


class MembershipFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Membership

    idol = factory.SubFactory(IdolFactory)
    group = factory.SubFactory(GroupFactory)
    started = datetime.date.today() - datetime.timedelta(days=365)

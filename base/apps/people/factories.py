import datetime
import factory

from django.template.defaultfilters import slugify

from . import models


class PersonFactory(factory.django.DjangoModelFactory):
    romanized_family_name = factory.Sequence(lambda i: 'family#%s' % i)
    romanized_given_name = factory.Sequence(lambda i: 'given#%s' % i)
    romanized_name = factory.LazyAttribute(lambda f: '%s %s' % (f.romanized_family_name, f.romanized_given_name))
    slug = factory.LazyAttribute(lambda f: slugify(f.romanized_name))

    class Meta:
        model = models.Person
        abstract = True


class IdolFactory(PersonFactory):
    birthdate = datetime.date.today() - datetime.timedelta(days=365 * 18)

    class Meta:
        model = models.Idol


class StaffFactory(PersonFactory):
    class Meta:
        model = models.Staff


class GroupFactory(factory.django.DjangoModelFactory):
    romanized_name = factory.Sequence(lambda i: 'group#%s' % i)
    slug = factory.LazyAttribute(lambda s: slugify(s.romanized_name))
    started = datetime.date.today() - datetime.timedelta(days=365)

    class Meta:
        model = models.Group


class MembershipFactory(factory.django.DjangoModelFactory):
    idol = factory.SubFactory(IdolFactory)
    group = factory.SubFactory(GroupFactory)
    started = datetime.date.today() - datetime.timedelta(days=365)

    class Meta:
        model = models.Membership


class LeadershipFactory(MembershipFactory):
    is_leader = True
    leadership_started = datetime.date.today() - datetime.timedelta(days=365)


class GroupshotFactory(factory.django.DjangoModelFactory):
    subject = factory.SubFactory(GroupFactory)
    taken = datetime.date.today()

    class Meta:
        model = models.Groupshot


class HeadshotFactory(factory.django.DjangoModelFactory):
    subject = factory.SubFactory(IdolFactory)
    taken = datetime.date.today()

    class Meta:
        model = models.Headshot

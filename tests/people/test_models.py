# -*- coding: utf-8 -*-
import datetime
import pytest

from components.people.models import (Fact, Group, Groupshot, Headshot, Idol,
    Membership, Staff)
from components.people.factories import (FactFactory, GroupFactory,
    GroupshotFactory, HeadshotFactory, IdolFactory, MembershipFactory,
    StaffFactory)

pytestmark = pytest.mark.django_db


class TestGroups:
    def test_group_factory(self):
        factory = GroupFactory()
        assert isinstance(factory, Group)
        assert 'group' in factory.romanized_name
        assert factory.identifier == 'group'

    def test_group_get_absolute_url(self, client):
        factory = GroupFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_group_age(self):
        active = GroupFactory(started=datetime.date.today() - datetime.timedelta(days=366))
        inactive = GroupFactory(started=datetime.date.today() - datetime.timedelta(days=366), ended=datetime.date.today())
        assert active.age == 1
        assert active.age_in_days == 366
        assert inactive.age == 1
        assert inactive.age_in_days == 366


class TestIdols:
    def test_idol_factory(self):
        factory = IdolFactory()
        assert isinstance(factory, Idol)
        assert factory.identifier == 'idol'
        assert 'family' in factory.romanized_family_name
        assert 'given' in factory.romanized_given_name

    def test_idol_get_absolute_url(self, client):
        factory = IdolFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_idol_name_with_alias(self):
        factory = IdolFactory(alias=u'ジュンジュン', romanized_alias='JunJun')
        assert factory.name == u'ジュンジュン'
        assert factory.romanized_name == 'JunJun'

    def test_idol_gaijin(self):
        nihonjin = IdolFactory()
        assert not nihonjin.is_gaijin()

        gaijin = IdolFactory(romanized_family_name='Sandbo', romanized_given_name='Lehua')
        assert gaijin.is_gaijin()
        assert gaijin.romanized_name == 'Lehua Sandbo'


class TestStaff:
    def test_staff_factory(self):
        factory = StaffFactory()
        assert isinstance(factory, Staff)
        assert 'family' in factory.romanized_family_name
        assert 'given' in factory.romanized_given_name


class TestMemberships:
    def test_membership_factory(self):
        factory = MembershipFactory()
        assert isinstance(factory, Membership)
        assert isinstance(factory.group, Group)
        assert isinstance(factory.idol, Idol)

    def test_membership_is_active(self):
        active = MembershipFactory()
        assert active.is_active()

        impending_inactive = MembershipFactory(ended=datetime.date.today() + datetime.timedelta(days=1))
        assert impending_inactive.is_active()

        inactive = MembershipFactory(ended=datetime.date.today() - datetime.timedelta(days=1))
        assert not inactive.is_active()

    def test_membership_days_before_starting(self):
        factory = MembershipFactory()
        assert factory.days_before_starting() == 0

    def test_membership_days_before_ending(self):
        factory = MembershipFactory(ended=datetime.date.today())
        assert factory.days_before_ending() == 365

    def test_membership_tenure_in_days(self):
        active = MembershipFactory()
        assert active.tenure_in_days() == 365

        inactive = MembershipFactory(ended=datetime.date.today() - datetime.timedelta(days=1))
        assert inactive.tenure_in_days() == 364


class TestGroupshots:
    def test_groupshot_factory(self):
        factory = GroupshotFactory()
        assert isinstance(factory, Groupshot)
        assert isinstance(factory.group, Group)


class TestHeadshots:
    def test_headshot_factory(self):
        factory = HeadshotFactory()
        assert isinstance(factory, Headshot)
        assert isinstance(factory.idol, Idol)


class TestFacts:
    def test_fact_factory(self):
        factory = FactFactory()
        assert isinstance(factory, Fact)

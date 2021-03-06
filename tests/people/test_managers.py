# -*- coding: utf-8 -*-
import datetime
import pytest

from apps.people.constants import CLASSIFICATIONS, SCOPE, STATUS
from apps.people.factories import (GroupFactory, IdolFactory,
    MembershipFactory)
from apps.people.models import Group, Idol, Membership

pytestmark = pytest.mark.django_db


@pytest.fixture
def hello_project():
    kwargs = {
        'classification': CLASSIFICATIONS.major,
        'scope': SCOPE.hp,
        'status': STATUS.active
    }

    return [
        GroupFactory(romanized_name='Morning Musume', **kwargs),
        GroupFactory(romanized_name='Berryz Koubou', **kwargs),
        GroupFactory(romanized_name='C-ute', **kwargs),
        GroupFactory(romanized_name='S/mileage', **kwargs),
        GroupFactory(romanized_name='Hello Pro Kenshuusei', **kwargs),
        GroupFactory(romanized_name='Juice=Juice', **kwargs)
    ]


class TestIdols:
    @pytest.fixture
    def status(self):
        idols = []
        [idols.append(IdolFactory(status=STATUS.active)) for i in xrange(3)]
        [idols.append(IdolFactory(status=STATUS.former)) for i in xrange(2)]
        return idols

    def test_active(self, status):
        assert len(Idol.objects.active()) == 3

    def test_inactive(self, status):
        assert len(Idol.objects.inactive()) == 2

    def test_hello_project(self, hello_project):
        for group in hello_project:
            idol = IdolFactory()
            membership = MembershipFactory(idol=idol, group=group, started=datetime.date.today())
            idol.primary_membership = membership
            idol.save()
        assert len(Idol.objects.hello_project()) == 6

    def test_average_age(self):
        idols = [IdolFactory(birthdate=datetime.date.today() - datetime.timedelta(days=365)) for i in xrange(10)]
        for idol in idols:
            assert idol.age == 1
        assert Idol.objects.average_age() == 1

    def test_average_height(self):
        [IdolFactory(height=150) for i in xrange(10)]
        assert Idol.objects.average_height() == 150


class TestGroups:
    @pytest.fixture
    def status(self):
        groups = [
            GroupFactory(),
            GroupFactory(ended=datetime.date.today() + datetime.timedelta(days=30)),
            GroupFactory(ended=datetime.date.today() - datetime.timedelta(days=30))
        ]
        return groups

    def test_active(self, status):
        assert len(Group.objects.active()) == 2

    def test_targeted_active(self, status):
        assert len(Group.objects.active(target=datetime.date.today())) == 2

    def test_inactive(self, status):
        assert len(Group.objects.inactive()) == 1

    def test_hello_project(self, hello_project):
        assert len(Group.objects.hello_project()) == len(hello_project)


class TestMemberships:
    def test_active(self):
        group = GroupFactory()
        [MembershipFactory(ended=datetime.date.today() + datetime.timedelta(days=30)) for i in xrange(5)]
        [MembershipFactory(group=group) for i in xrange(5)]
        assert len(Membership.objects.active()) == 10
        assert len(Membership.objects.active(for_group=group)) == 5

    def test_inactive(self):
        [MembershipFactory(ended=datetime.date.today() - datetime.timedelta(days=30)) for i in xrange(5)]
        [MembershipFactory(ended=datetime.date.today()) for i in xrange(5)]
        assert len(Membership.objects.inactive()) == 5

    def test_inactive_leaders(self):
        [MembershipFactory(is_leader=True, leadership_ended=datetime.date.today() - datetime.timedelta(days=30)) for i in xrange(5)]
        [MembershipFactory(is_leader=True, leadership_ended=datetime.date.today()) for i in xrange(5)]
        assert len(Membership.objects.inactive_leaders()) == 10

    def test_active_lineup(self):
        group = GroupFactory()
        [MembershipFactory(ended=datetime.date.today() + datetime.timedelta(days=30)) for i in xrange(5)]
        [MembershipFactory(group=group) for i in xrange(5)]
        assert len(Membership.objects.lineup()) == 10

    def test_inactive_lineup(self):
        group = GroupFactory(ended=datetime.date.today())
        [MembershipFactory(ended=datetime.date.today()) for i in xrange(5)]
        assert len(Membership.objects.lineup(target=group.ended)) == 5

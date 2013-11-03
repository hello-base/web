# -*- coding: utf-8 -*-
import datetime
import pytest

from components.people.constants import CLASSIFICATIONS, SCOPE, STATUS
from components.people.factories import (GroupFactory, IdolFactory,
    MembershipFactory)
from components.people.models import Group, Idol

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

    def test_active_manager(self, status):
        assert len(Idol.objects.active()) == 3

    def test_inactive_manager(self, status):
        assert len(Idol.objects.inactive()) == 2

    def test_hello_project_manager(self, hello_project):
        for group in hello_project:
            idol = IdolFactory()
            membership = MembershipFactory(idol=idol, group=group, started=datetime.date.today())
            idol.primary_membership = membership
            idol.save()
        assert len(Idol.objects.hello_project()) == 6


class TestGroups:
    @pytest.fixture
    def status(self):
        groups = [
            GroupFactory(),
            GroupFactory(ended=datetime.date.today() + datetime.timedelta(days=30)),
            GroupFactory(ended=datetime.date.today() - datetime.timedelta(days=30))
        ]
        return groups

    def test_active_manager(self, status):
        assert len(Group.objects.active()) == 2

    def test_inactive_manager(self, status):
        assert len(Group.objects.inactive()) == 1

    def test_hello_project_manager(self, hello_project):
        assert len(Group.objects.hello_project()) == len(hello_project)

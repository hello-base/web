# -*- coding: utf-8 -*-
import datetime
import pytest

from components.people.constants import STATUS
from components.people.factories import GroupFactory, IdolFactory
from components.people.models import Group, Idol

pytestmark = pytest.mark.django_db


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

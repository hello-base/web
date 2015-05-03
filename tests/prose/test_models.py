# -*- coding: utf-8 -*-
import pytest

from apps.prose.factories import FactFactory
from apps.prose.models import Fact
from apps.people.factories import GroupFactory, IdolFactory

pytestmark = pytest.mark.django_db


class TestFacts:
    def test_factory(self):
        group = GroupFactory()
        factory = FactFactory(group=group)
        assert isinstance(factory, Fact)
        assert 'group' in repr(factory)

    def test_factory_parent(self):
        group = GroupFactory()
        group_fact = FactFactory(group=group)
        assert group_fact.parent == group

        idol = IdolFactory()
        idol_fact = FactFactory(idol=idol)
        assert idol_fact.parent == idol

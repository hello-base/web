# -*- coding: utf-8 -*-
import pytest

from components.appearances.factories import CardFactory
from components.appearances.models import Card
from components.people.factories import GroupFactory, IdolFactory

pytestmark = pytest.mark.django_db


class TestCards:
    def test_group_name(self):
        group = GroupFactory(name=u'モーニング娘。')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_group_name=u'AKB48')
        assert card1.group_name == u'モーニング娘。'
        assert card2.group_name == u'AKB48'

    def test_romanized_group_name(self):
        group = GroupFactory(romanized_name='Morning Musume')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_group_romanized_name='AKB48')
        assert card1.group_name == 'Morning Musume'
        assert card2.group_name == 'AKB48'

    def test_model_name(self):
        idol = GroupFactory(name=u'道重 さゆみ')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_model_name=u'秋元 才加')
        assert card1.group_name == u'道重 さゆみ'
        assert card2.group_name == u'秋元 才加'

    def test_romanized_model_name(self):
        group = GroupFactory(name='Michishige Sayumi')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_model_romanized_name='Akimoto Sayaka')
        assert card1.group_name == 'Michishige Sayumi'
        assert card2.group_name == 'Akimoto Sayaka'

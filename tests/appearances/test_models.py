# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from base.apps.appearances.factories import CardFactory
from base.apps.people.factories import GroupFactory, IdolFactory

pytestmark = pytest.mark.django_db


class TestCards:
    def test_group_name(self):
        group = GroupFactory(name='モーニング娘。')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_group_name='AKB48')
        assert card1.group_name == 'モーニング娘。'
        assert card2.group_name == 'AKB48'

    def test_romanized_group_name(self):
        group = GroupFactory(romanized_name='Morning Musume')
        card1 = CardFactory(group=group)
        card2 = CardFactory(other_group_romanized_name='AKB48')
        assert card1.group_romanized_name == 'Morning Musume'
        assert card2.group_romanized_name == 'AKB48'

    def test_model_name(self):
        model = IdolFactory(family_name='道重', given_name='さゆみ')
        card1 = CardFactory(hp_model=model)
        card2 = CardFactory(other_model_name='秋元才加')
        assert card1.model_name == '道重さゆみ'
        assert card2.model_name == '秋元才加'

    def test_romanized_model_name(self):
        model = IdolFactory(
            family_name='道重', given_name='さゆみ',
            romanized_family_name='Michishige', romanized_given_name='Sayumi'
        )
        card1 = CardFactory(hp_model=model)
        card2 = CardFactory(other_model_romanized_name='Akimoto Sayaka')
        assert card1.model_romanized_name == 'Michishige Sayumi'
        assert card2.model_romanized_name == 'Akimoto Sayaka'

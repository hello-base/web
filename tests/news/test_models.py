# -*- coding: utf-8 -*-
import pytest

from base.apps.news.models import Item, ItemImage, Update
from base.apps.news.factories import (ItemFactory, ItemImageFactory,
    UpdateFactory)

pytestmark = pytest.mark.django_db


class TestItems:
    def test_factory(self):
        factory = ItemFactory()
        assert isinstance(factory, Item)


class TestItemImages:
    def test_factory(self):
        item = ItemFactory()
        factory = ItemImageFactory(parent=item)
        assert isinstance(factory, ItemImage)


class TestUpdates:
    def test_factory(self):
        item = ItemFactory()
        factory = UpdateFactory(parent=item)
        assert isinstance(factory, Update)

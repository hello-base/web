# -*- coding: utf-8 -*-
import datetime
import pytest

from django.core.exceptions import ValidationError

from base.apps.merchandise.goods.factories import GoodFactory, ShopFactory
from base.apps.merchandise.goods.models import Good

pytestmark = pytest.mark.django_db


class TestGoods:
    def test_date_validation(self):
        with pytest.raises(ValidationError) as execinfo:
            GoodFactory(
                available_from=datetime.date.today(),
                available_until=datetime.date.today() - datetime.timedelta(days=1),
            )
            message = u'The "Available Until" date is earlier than "Available From".'
            assert message in execinfo.execonly()

    def test_source_validation(self):
        with pytest.raises(ValidationError) as execinfo:
            GoodFactory()
            message = u'Goods must either originate from a shop or an event.'
            assert message in execinfo.execonly()

    def test_factory(self):
        factory = GoodFactory(
            name='test-good', romanized_name='test-good', category='lphoto',
            available_from=datetime.date.today() - datetime.timedelta(days=1),
            available_until=datetime.date.today(),
            shop=ShopFactory(),
        )
        assert isinstance(factory, Good)

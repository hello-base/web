# -*- coding: utf-8 -*-
import datetime
import pytest

from apps.correlations.utils import call_attributes

FIELDS = ['started']


def test_successful_attribute_call():
    class ProperlyAttributed(object):
        started = datetime.datetime.now()

    obj = ProperlyAttributed()
    assert call_attributes(obj, FIELDS)


def test_failing_attribute_call():
    class ImproperlyAttributed(object):
        timestamp = datetime.datetime.now()

    obj = ImproperlyAttributed()
    with pytest.raises(AttributeError):
        call_attributes(obj, FIELDS)

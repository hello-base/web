# -*- coding: utf-8 -*-
import datetime
import pytest

from bs4 import BeautifulSoup

from django.template import Template, Context

from components.correlations.models import Correlation
from components.people.factories import GroupFactory


@pytest.mark.django_db
def test_render_correlation():
    group = GroupFactory(started=datetime.date(2013, 1, 1))
    correlation = Correlation.objects.all()[0]
    out = Template(
        '{% load correlation_tags %}'
        '{% render_correlation correlation %}'
    ).render(Context({'correlation': correlation}))
    assert group.romanized_name in out
    assert len(BeautifulSoup(out).find_all('a')) == 1

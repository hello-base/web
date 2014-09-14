# -*- coding: utf-8 -*-
import datetime
import pytest

from django.core.urlresolvers import reverse

from base.apps.people.factories import GroupFactory


@pytest.mark.django_db
def test_happenings_by_year_view(client):
    [GroupFactory(started=datetime.date(2013, 1, 1)) for i in xrange(5)]
    response = client.get(reverse('happenings-by-year', kwargs={'year': 2013}))
    assert response.status_code == 200
    assert 'object_list' in response.context
    assert '2010s' in response.context['years']
    assert 'correlations/happenings_year.html' in [template.name for template in response.templates]

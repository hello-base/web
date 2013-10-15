import pytest

from django.core.urlresolvers import reverse

from components.people.models import Group, Idol, Membership, Staff


def test_group_detail_view(client):
    response = client.get(reverse('group-detail'))
    assert response.status_code == 200


def test_idol_detail_view(client):
    response = client.get(reverse('idol-detail'))
    assert response.status_code == 200

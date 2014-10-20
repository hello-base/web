# -*- coding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from base.apps.people import factories

pytestmark = pytest.mark.django_db


def test_api_group_list_view(client):
    response = client.get(reverse('api:group-list'))
    assert response.status_code == 200


def test_api_group_detail_view(client):
    group = factories.GroupFactory()
    response = client.get(reverse('api:group-detail', kwargs={'slug': group.slug}))
    assert response.status_code == 200


def test_api_group_members_view(client):
    group = factories.GroupFactory()
    response = client.get(reverse('api:group-members', kwargs={'slug': group.slug}))
    assert response.status_code == 200


def test_api_active_group_members_view(client):
    group = factories.GroupFactory()
    response = client.get(reverse('api:group-members-active', kwargs={'slug': group.slug}))
    assert response.status_code == 200


def test_api_inactive_group_members_view(client):
    group = factories.GroupFactory()
    response = client.get(reverse('api:group-members-inactive', kwargs={'slug': group.slug}))
    assert response.status_code == 200


def test_api_idol_list_view(client):
    response = client.get(reverse('api:idol-list'))
    assert response.status_code == 200


def test_api_idol_detail_view(client):
    idol = factories.IdolFactory()
    response = client.get(reverse('api:idol-detail', kwargs={'slug': idol.slug}))
    assert response.status_code == 200

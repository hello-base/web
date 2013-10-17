import pytest

from components.people.models import Group, Idol, Membership, Staff
from components.people.factories import (GroupFactory, IdolFactory,
    MembershipFactory, StaffFactory)


pytestmark = pytest.mark.django_db

def test_group_factory():
    factory = GroupFactory()
    assert isinstance(factory, Group)
    assert 'group' in factory.romanized_name


def test_group_get_absolute_url(client):
    factory = GroupFactory()
    response = client.get(factory.get_absolute_url())
    assert response.status_code == 200


def test_idol_factory():
    factory = IdolFactory()
    assert isinstance(factory, Idol)
    assert 'family' in factory.romanized_family_name
    assert 'given' in factory.romanized_given_name


def test_idol_get_absolute_url(client):
    factory = IdolFactory()
    response = client.get(factory.get_absolute_url())
    assert response.status_code == 200


def test_staff_factory():
    factory = StaffFactory()
    assert isinstance(factory, Staff)
    assert 'family' in factory.romanized_family_name
    assert 'given' in factory.romanized_given_name


def test_membership_factory():
    factory = MembershipFactory()
    assert isinstance(factory, Membership)
    assert isinstance(factory.group, Group)
    assert isinstance(factory.idol, Idol)

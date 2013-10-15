import pytest

from components.people.models import Group, Idol, Membership, Staff
from components.people.factories import (GroupFactory, IdolFactory,
    MembershipFactory, StaffFactory)


@pytest.mark.django_db
def test_group_factory():
    factory = GroupFactory()
    assert isinstance(factory, Group)
    assert 'group' in factory.romanized_name


@pytest.mark.django_db
def test_idol_factory():
    factory = IdolFactory()
    assert isinstance(factory, Idol)
    assert 'family' in factory.romanized_family_name
    assert 'given' in factory.romanized_given_name


@pytest.mark.django_db
def test_idol_romanized_name():
    pass


@pytest.mark.django_db
def test_staff_factory():
    factory = StaffFactory()
    assert isinstance(factory, Staff)
    assert 'family' in factory.romanized_family_name
    assert 'given' in factory.romanized_given_name


@pytest.mark.django_db
def test_membership_factory():
    factory = MembershipFactory()
    assert isinstance(factory, Membership)
    assert isinstance(factory.group, Group)
    assert isinstance(factory.idol, Idol)

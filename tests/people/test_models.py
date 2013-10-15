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
    assert 'idol' in factory.romanized_name


@pytest.mark.django_db
def test_membership_factory():
    factory = MembershipFactory()
    assert isinstance(factory, Membership)
    assert isinstance(factory.group, Group)
    assert isinstance(factory.idol, Idol)

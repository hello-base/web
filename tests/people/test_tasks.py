import pytest

from components.merchandise.music.factories import SingleFactory
from components.people.constants import CLASSIFICATIONS
from components.people.factories import (GroupFactory, MembershipFactory,
    IdolFactory)
from components.people.tasks import render_participants

pytestmark = pytest.mark.django_db


@pytest.fixture
def release():
    return SingleFactory()


def test_render_idols(release):
    release.idols.add(*[IdolFactory() for i in xrange(5)])
    render_participants(release)
    assert len(release.participating_idols.all()) == 5
    assert not release.participating_groups.all()

    # Run it again to make sure the participating_* relations are cleared
    # on a second run-through.
    release.idols.clear()
    release.idols.add(*[IdolFactory() for i in xrange(3)])
    render_participants(release)
    assert len(release.participating_idols.all()) == 3
    assert not release.participating_groups.all()


def test_render_group(release):
    group = GroupFactory()
    idols = [IdolFactory() for i in xrange(3)]
    [MembershipFactory(group=group, idol=idols[i]) for i in xrange(3)]
    release.groups.add(group)
    release.idols.add(*idols)
    render_participants(release)
    assert len(release.participating_groups.all()) == 1
    assert not release.participating_idols.all()


def test_render_supergroup(release):
    supergroup = GroupFactory(classification=CLASSIFICATIONS.supergroup)
    groups = [GroupFactory() for i in xrange(3)]
    release.groups.add(supergroup)
    release.groups.add(*groups)
    render_participants(release)
    assert len(release.participating_groups.all()) == 1
    assert release.participating_groups.all()[0] == supergroup
    assert not release.participating_idols.all()

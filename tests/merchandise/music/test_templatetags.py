import pytest

from bs4 import BeautifulSoup

from django.template import Template, Context

from components.merchandise.music.factories import SingleFactory
from components.people.constants import CLASSIFICATIONS
from components.people.factories import (GroupFactory, MembershipFactory,
    IdolFactory)

pytestmark = pytest.mark.django_db


@pytest.fixture
def release():
    return SingleFactory()


def test_soloist(release):
    # When a soloist is the subject object, it should not render a result.
    idol = IdolFactory()
    group = GroupFactory(romanized_name='Soloist')
    membership = MembershipFactory(idol=idol, group=group)
    idol.primary_membership = membership
    release.participants = [soloist]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': soloist}))
    assert out.rstrip('\n') == ''


def test_solo_work(release):
    # When an idol is the subject object and the only participant in a release,
    # "Solo Work" should be rendered.
    subject = IdolFactory()
    release.participants = [subject]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert out.rstrip('\n') == '<span class="pill status-solo">Solo Work</span>'


def test_idols(release):
    # When an idol is the subject object and is not the only participant in
    # a release, "with" should be rendered along with the other participants.
    subject = IdolFactory()
    release.participants = [IdolFactory() for i in xrange(3)]
    release.participants.append(subject)
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'with' in out
    assert len(BeautifulSoup(out).find_all('a')) == 3


def test_idols_and_secondary_groups(release):
    # When an idol is the subject object and a participating group is not their
    # primary group, "for" should be rendered along with the group.
    subject = IdolFactory()
    primary_group = GroupFactory()
    primary_membership = MembershipFactory(idol=subject, group=primary_group)
    subject.primary_membership = primary_membership
    secondary_group = GroupFactory()
    secondary_membership = MembershipFactory(idol=subject, group=secondary_group)
    release.participants = [subject, secondary_group]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'for' in out
    assert len(BeautifulSoup(out).find_all('a')) == 1


def test_group(release):
    subject = GroupFactory()
    release.participants = [subject]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert out.rstrip('\n') == ''


def test_groups(release):
    subject = GroupFactory()
    release.participants = [subject]
    release.participants.extend([GroupFactory() for i in xrange(3)])
    release.participants.extend([IdolFactory() for i in xrange(3)])
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'with' in out
    assert len(BeautifulSoup(out).find_all('a')) == 6


def test_supergroup(release):
    subject = GroupFactory()
    supergroup = GroupFactory(classification=CLASSIFICATIONS.supergroup)
    release.participants = [subject, supergroup]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'for' in out
    assert len(BeautifulSoup(out).find_all('a')) == 1

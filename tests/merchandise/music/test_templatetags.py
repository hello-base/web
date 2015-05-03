import pytest

from bs4 import BeautifulSoup

from django.template import Template, Context

from apps.merchandise.music.factories import SingleFactory
from apps.people.constants import CLASSIFICATIONS
from apps.people.factories import (GroupFactory, MembershipFactory,
    IdolFactory)

pytestmark = pytest.mark.django_db


@pytest.fixture
def release():
    return SingleFactory()


def test_soloist(release):
    # When a soloist is the subject object, it should not render a result.
    subject = IdolFactory()
    group = GroupFactory(romanized_name='Soloist')
    membership = MembershipFactory(idol=subject, group=group)
    subject.primary_membership = membership
    release.participants = [subject]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
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


def test_idols_and_single_groups(release):
    # When an idol is the subject object and there is a single participating
    # group, it should not render a result.
    subject = IdolFactory()
    primary_group = GroupFactory()
    subject.primary_membership = MembershipFactory(idol=subject, group=primary_group)
    release.participants = [primary_group]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert out.rstrip('\n') == ''


def test_idols_and_secondary_groups(release):
    # When an idol is the subject object and a participating group is not their
    # primary group, "for" should be rendered along with the group.
    subject = IdolFactory()
    primary_group = GroupFactory()
    subject.primary_membership = MembershipFactory(idol=subject, group=primary_group)
    secondary_group = GroupFactory()
    MembershipFactory(idol=subject, group=secondary_group)
    release.participants = [subject, secondary_group]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'for' in out
    assert len(BeautifulSoup(out).find_all('a')) == 1


def test_supergroup_with_idol_context(release):
    subject = IdolFactory()
    subject.primary_membership = MembershipFactory(idol=subject)
    subject.save()
    supergroup = GroupFactory(classification=CLASSIFICATIONS.supergroup)
    MembershipFactory(idol=subject, group=supergroup)
    release.participants = [supergroup]
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
    release.participants = [subject, GroupFactory(), IdolFactory()]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'with' in out
    assert len(BeautifulSoup(out).find_all('a')) == 2


def test_supergroup_with_group_context(release):
    subject = GroupFactory()
    supergroup = GroupFactory(classification=CLASSIFICATIONS.supergroup)
    release.participants = [subject, supergroup]
    out = Template(
        '{% load music_tags %}'
        '{% contextual_participants release=release context=object %}'
    ).render(Context({'release': release, 'object': subject}))
    assert 'for' in out
    assert len(BeautifulSoup(out).find_all('a')) == 1

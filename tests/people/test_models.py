# -*- coding: utf-8 -*-
import datetime
import pytest

from apps.people.models import (Group, Groupshot, Headshot, Idol,
    Membership, Staff)
from apps.people.factories import (GroupFactory, GroupshotFactory,
    HeadshotFactory, IdolFactory, LeadershipFactory, MembershipFactory,
    StaffFactory)

today = datetime.date.today()
delta = datetime.timedelta(days=1)
pytestmark = pytest.mark.django_db


class TestGroups:
    def test_factory(self):
        factory = GroupFactory()
        assert isinstance(factory, Group)
        assert 'group' in factory.romanized_name
        assert factory.identifier == 'group'

    def test_get_absolute_url(self, client):
        factory = GroupFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_age(self):
        active = GroupFactory(started=today - datetime.timedelta(days=366))
        inactive = GroupFactory(started=today - datetime.timedelta(days=366), ended=today)
        assert active.age == 1
        assert active.age_in_days == 366
        assert inactive.age == 1
        assert inactive.age_in_days == 366

    def test_targeted_is_active(self):
        targeted_active = GroupFactory()
        assert targeted_active.is_active(target=today)

        targeted_inactive = GroupFactory(ended=today - delta)
        assert not targeted_inactive.is_active(target=today)

        targeted_upcoming = GroupFactory(started=today + delta)
        assert not targeted_upcoming.is_active(target=today)

    def test_supergroup_subgroups(self):
        supergroup = GroupFactory()
        for i in xrange(3):
            supergroup.groups.add(GroupFactory(started=today - datetime.timedelta(i)))
        assert supergroup.groups.count() > 0
        assert supergroup.groups.all()[0] == supergroup.groups.order_by('started')[0]

    def test_generations(self):
        group = GroupFactory()
        idols = [IdolFactory() for i in xrange(3)]
        [
            MembershipFactory(
                group=group, idol=idols[i], generation=i + 1
            ) for i in xrange(3)
        ]

        generations = group.generations()
        assert len(generations) == 3
        for k, v in generations.iteritems():
            assert isinstance(k, int)
            assert len(v) == 1

    def test_generations_failure(self):
        group = GroupFactory()
        idols = [IdolFactory() for i in xrange(3)]
        [MembershipFactory(group=group, idol=idols[i]) for i in xrange(3)]
        assert not group.generations()


class TestIdols:
    def test_factory(self):
        factory = IdolFactory()
        assert isinstance(factory, Idol)
        assert factory.identifier == 'idol'
        assert 'family' in factory.romanized_family_name
        assert 'given' in factory.romanized_given_name

    def test_get_absolute_url(self, client):
        factory = IdolFactory()
        response = client.get(factory.get_absolute_url())
        assert response.status_code == 200

    def test_name_with_alias(self):
        factory = IdolFactory(alias=u'ジュンジュン', romanized_alias='JunJun')
        assert factory.name == u'ジュンジュン'
        assert factory.romanized_name == 'JunJun'

    def test_gaijin(self):
        nihonjin = IdolFactory(family_name=u'譜久村', given_name=u'聖')
        assert not nihonjin.is_gaijin()

        gaijin = IdolFactory(romanized_family_name='Sandbo', romanized_given_name='Lehua')
        assert gaijin.is_gaijin()
        assert gaijin.romanized_name == 'Lehua Sandbo'


class TestStaff:
    def test_factory(self):
        factory = StaffFactory()
        assert isinstance(factory, Staff)
        assert 'family' in factory.romanized_family_name
        assert 'given' in factory.romanized_given_name


class TestMemberships:
    def test_factory(self):
        factory = MembershipFactory()
        assert isinstance(factory, Membership)
        assert isinstance(factory.group, Group)
        assert isinstance(factory.idol, Idol)
        assert 'family' and 'group' in repr(factory)

    def test_primary_membership_switching(self):
        idol = IdolFactory()
        membership1 = MembershipFactory(idol=idol, is_primary=True)
        assert idol.primary_membership == membership1

        membership1.is_primary = False
        membership1.save()
        membership2 = MembershipFactory(idol=idol, is_primary=True)
        assert idol.primary_membership == membership2

    def test_is_active(self):
        active = MembershipFactory()
        assert active.is_active()

        impending_inactive = MembershipFactory(ended=today + delta)
        assert impending_inactive.is_active()

        inactive = MembershipFactory(ended=today - delta)
        assert not inactive.is_active()

    def test_targeted_is_active(self):
        targeted_active = MembershipFactory()
        assert targeted_active.is_active(target=today)

        targeted_inactive = MembershipFactory(ended=today - delta)
        assert not targeted_inactive.is_active(target=today)

        targeted_upcoming = MembershipFactory(started=today + delta)
        assert not targeted_upcoming.is_active(target=today)

    def test_days_before_starting(self):
        factory = MembershipFactory()
        assert factory.days_before_starting() == 0

    def test_days_before_ending(self):
        active = MembershipFactory()
        assert not active.days_before_ending()

        inactive = MembershipFactory(ended=today)
        assert inactive.days_before_ending() == 365

    def test_tenure_in_days(self):
        active = MembershipFactory()
        assert active.tenure_in_days() == 365

        inactive = MembershipFactory(ended=today - delta)
        assert inactive.tenure_in_days() == 364

    def test_days_before_becoming_leader(self):
        member = MembershipFactory()
        assert not member.days_before_becoming_leader()

        leader = LeadershipFactory()
        assert leader.days_before_becoming_leader() == 0

    def test_leadership_tenure(self):
        member = MembershipFactory()
        assert not member.leadership_tenure()

        active_leader = LeadershipFactory()
        quirk = active_leader.leadership_tenure().replace(u'\xa0', ' ')
        assert quirk == u'1 year'

        inactive_leader = LeadershipFactory(leadership_ended=today - delta)
        quirk = inactive_leader.leadership_tenure().replace(u'\xa0', ' ')
        assert quirk == u'12 months'

    def test_leadership_tenure_in_days(self):
        member = MembershipFactory()
        assert not member.leadership_tenure_in_days()

        active_leader = LeadershipFactory()
        assert active_leader.leadership_tenure_in_days() == 365

        inactive_leader = LeadershipFactory(leadership_ended=today - delta)
        assert inactive_leader.leadership_tenure_in_days() == 364

    def test_standing(self):
        active_member = MembershipFactory()
        assert active_member.standing == 'Member'

        impending_inactive_member = MembershipFactory(ended=today + delta)
        assert impending_inactive_member.standing == 'Member'

        inactive_member = MembershipFactory(ended=today - delta)
        assert inactive_member.standing == 'Former member'

        active_leader = LeadershipFactory()
        assert active_leader.standing == 'Leader'

        inactive_leader = LeadershipFactory(leadership_ended=today - delta)
        assert inactive_leader.standing == 'Former leader'

        group = GroupFactory(romanized_name='Soloist')
        soloist = MembershipFactory(group=group)
        assert soloist.standing == 'Soloist'


class TestGroupshots:
    def test_factory(self):
        factory = GroupshotFactory()
        assert isinstance(factory, Groupshot)
        assert isinstance(factory.subject, Group)
        assert 'Photo of' and 'group' in repr(factory)


class TestHeadshots:
    def test_factory(self):
        factory = HeadshotFactory()
        assert isinstance(factory, Headshot)
        assert isinstance(factory.subject, Idol)
        assert 'Photo of' and 'family' in repr(factory)

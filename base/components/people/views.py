from collections import defaultdict
from operator import attrgetter

from django.views.generic import ListView, DetailView, TemplateView

from ohashi.shortcuts import get_object_or_none

from components.accounts.views import QuicklinksMixin
from .models import Group, Idol, Membership, Staff


class GroupDetailView(QuicklinksMixin, DetailView):
    queryset = Group.objects.all()
    template_name = 'people/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)

        # We need to split memberships into four groups. The active
        # leader, the active members, the former members and the
        # former leaders.
        memberships = self.object.memberships.order_by('started', 'idol__birthdate').select_related('idol', 'group')
        context['memberships'] = {
            'active': [m for m in memberships if m.ended is None],
            'active_count': len([m for m in memberships if m.ended is None]),
            'inactive': [m for m in memberships if m.ended],
            'inactive_count': len([m for m in memberships if m.ended]),
            'leader': get_object_or_none(Membership.objects.select_related('idol'), group=self.object.pk, ended__isnull=True, is_leader=True),
            'leaders': sorted([m for m in memberships if m.ended and m.is_leader and m.leadership_started is not None], key=attrgetter('leadership_started')),
            'leader_count': len([m for m in memberships if m.ended and m.is_leader and m.leadership_started is not None]),

            # 'active': [m for m in memberships if m.ended is None and m.is_leader == False],
            # 'inactive': [m for m in memberships if m.ended and m.is_leader == False],
        }

        context['albums'] = self.object.albums.prefetch_related('editions', 'participating_idols', 'participating_groups')
        context['events'] = self.object.events.all()
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class IdolDetailView(QuicklinksMixin, DetailView):
    model = Idol
    template_name = 'people/idol_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IdolDetailView, self).get_context_data(**kwargs)
        context['albums'] = self.object.albums.prefetch_related('editions', 'participating_idols', 'participating_groups')
        context['events'] = self.object.events.all()
        context['memberships'] = self.object.memberships.select_related('group')[1:]
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class StaffDetailView(DetailView):
    queryset = Staff.objects.all()
    template_name = ''


class HelloProjectDetailView(TemplateView):
    idols = Idol.objects.hello_project().select_related('primary_membership__group')
    groups = Group.objects.hello_project()
    template_name = 'people/overrides/hello_project.html'

    def process_groups(self):
        d = defaultdict(list)
        for group in self.groups:
            d[group] = [idol for idol in self.idols if idol.primary_membership.group == group]
        return dict(d)

    def get_context_data(self, **kwargs):
        context = super(HelloProjectDetailView, self).get_context_data(**kwargs)
        context['groups'] = self.process_groups()
        context['statistics'] = {
            'average_age': self.idols.average_age()
        }
        return context

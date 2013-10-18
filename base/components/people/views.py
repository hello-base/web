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
        memberships = self.object.memberships.order_by('started').select_related('idol', 'group')
        context['memberships'] = {
            'active': [m for m in memberships if m.ended is None],
            'active_count': len([m for m in memberships if m.ended is None]),
            'inactive': [m for m in memberships if m.ended],

            # 'active': [m for m in memberships if m.ended is None and m.is_leader == False],
            # 'inactive': [m for m in memberships if m.ended and m.is_leader == False],
            # 'leader': get_object_or_none(Membership.objects.select_related('idol'), group=self.object.pk, ended__isnull=True, is_leader=True),
            # 'leaders': sorted([m for m in memberships if m.ended and m.is_leader and m.leadership_started != None], key=attrgetter('leadership_started')),
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

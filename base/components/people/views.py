from operator import attrgetter

from django.views.generic import ListView, DetailView, TemplateView

from braces.views import PrefetchRelatedMixin, SelectRelatedMixin
from ohashi.shortcuts import get_object_or_none

# from components.merchandise.music import constants as music
from .models import Group, Idol, Membership, Staff
# from .utils import attach_primary_groups


class GroupBrowseView(ListView):
    queryset = Group.objects.order_by('slug')
    template_name = 'people/groups/group_browse.html'

    def get_context_data(self, **kwargs):
        context = super(GroupBrowseView, self).get_context_data(**kwargs)
        context['active_groups'] = Group.objects.active().order_by('classification', 'started')
        context['inactive_groups'] = Group.objects.inactive().order_by('classification')
        return context


class GroupDetailView(DetailView):
    queryset = Group.objects.all()
    template_name = 'people/groups/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)

        # We need to split memberships into four groups. The active
        # leader, the active members, the former members and the
        # former leaders.
        memberships = self.object.memberships.order_by('started').select_related('idol', 'group')
        context['memberships'] = {
            'active': [m for m in memberships if m.ended is None and m.is_leader == False],
            'active_count': len([m for m in memberships if m.ended is None]),
            'inactive': [m for m in memberships if m.ended and m.is_leader == False],
            'leader': get_object_or_none(Membership.objects.select_related('idol'), group=self.object.pk, ended__isnull=True, is_leader=True),
            'leaders': sorted([m for m in memberships if m.ended and m.is_leader and m.leadership_started != None], key=attrgetter('leadership_started')),
        }

        context['albums'] = self.object.albums.prefetch_related('editions', 'participating_idols', 'participating_groups')
        context['events'] = self.object.events.all()
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class GroupMembershipView(DetailView):
    queryset = Group.objects.all()
    template_name = 'people/groups/group_membership.html'


class IdolBrowseView(TemplateView):
    template_name = 'people/idols/idol_browse.html'

#     def get_context_data(self, **kwargs):
#         context = super(IdolBrowseView, self).get_context_data(**kwargs)

#         hello_project = Idol.objects.hello_project()
#         hello_project_roster = attach_primary_groups(hello_project.order_by('birthdate'))
#         context['hello_project'] = {
#             'roster': hello_project_roster,
#             'roster_count': hello_project.count(),

#             # Aggregations
#             'average_age': hello_project.average_age(),
#             'average_height': hello_project.average_height(),
#             'popular_bloodtype': hello_project.popular_bloodtype(),

#             # Superlatives
#             'most_junior_member': hello_project.most_junior_member(),
#             'most_senior_member': hello_project.most_senior_member(),
#             'tallest_member': hello_project.tallest_member(),
#             'shortest_member': hello_project.shortest_member(),
#             'oldest_member': hello_project.oldest_member(),
#             'youngest_member': hello_project.youngest_member(),
#         }

#         everybody_else = Idol.objects.everybody_else()
#         context['everybody_else'] = attach_primary_groups(everybody_else)
#         return context


class IdolDetailView(PrefetchRelatedMixin, DetailView):
    model = Idol
    prefetch_related = ['memberships__group']
    template_name = 'people/idols/idol_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IdolDetailView, self).get_context_data(**kwargs)
        context['albums'] = self.object.albums.prefetch_related('editions', 'participating_idols', 'participating_groups')
        context['events'] = self.object.events.all()
        context['memberships'] = self.object.memberships.select_related('group')[1:]
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class StaffBrowseView(ListView):
    queryset = Staff.objects.all()
    template_name = ''


class StaffDetailView(DetailView):
    queryset = Staff.objects.all()
    template_name = ''

from django.views.generic import ListView, DetailView, TemplateView

from braces.views import PrefetchRelatedMixin, SelectRelatedMixin

# from components.merchandise.music import constants as music
from .models import Group, Idol, Staff
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
        context['albums'] = self.object.albums.prefetch_related('editions', 'participating_idols', 'participating_groups')
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class GroupDiscographyView(DetailView):
    queryset = Group.objects.all()
    template_name = 'people/groups/group_discography.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDiscographyView, self).get_context_data(**kwargs)
        context['discography'] = sorted(construct_list_using_index(storage_key=music.OWNER_LIST_KEY % ('groups', self.object.id)), key=lambda x: x.released, reverse=True)
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
        context['memberships'] = self.object.memberships.select_related('group')[1:]
        context['singles'] = self.object.singles.prefetch_related('editions', 'participating_idols', 'participating_groups')
        return context


class IdolDiscographyView(DetailView):
    queryset = Idol.objects.all()
    template_name = 'people/idols/idol_discography.html'

    def get_context_data(self, **kwargs):
        context = super(IdolDiscographyView, self).get_context_data(**kwargs)
        context['discography'] = sorted(construct_list_using_index(storage_key=music.OWNER_LIST_KEY % ('idols', self.object.id)), key=lambda x: x.released, reverse=True)
        return context


class StaffBrowseView(ListView):
    queryset = Staff.objects.all()
    template_name = ''


class StaffDetailView(DetailView):
    queryset = Staff.objects.all()
    template_name = ''

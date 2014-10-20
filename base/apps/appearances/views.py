from django.views.generic import ListView, DetailView

from .models import Show, Episode, Magazine, Issue


class ShowListView(ListView):
    queryset = Show.objects.all()
    template_name = 'appearances/show_list.html'


class ShowDetailView(DetailView):
    queryset = Show.objects.all()
    template_name = 'appearances/show_detail.html'


class EpisodeDetailView(DetailView):
    queryset = Episode.objects.all()
    template_name = 'appearances/episode_detail.html'


class MagazineListView(ListView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine_list.html'


class MagazineDetailView(DetailView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine_detail.html'


class IssueDetailView(DetailView):
    queryset = Issue.objects.all()
    template_name = 'appearances/issue_detail.html'

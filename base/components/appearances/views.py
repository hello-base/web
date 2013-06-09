from django.views.generic import ListView, DetailView, TemplateView

from .models import Show, Episode, Magazine, Issue


class ShowListView(ListView):
    queryset = Show.objects.all()
    template_name = 'appearances/show-list.html'


class ShowDetailView(DetailView):
    queryset = Show.objects.all()
    template_name = 'appearances/show-detail.html'


class EpisodeDetailView(DetailView):
    queryset = Episode.objects.all()
    template_name = 'appearances/episode-detail.html'


class MagazineListView(ListView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine-list.html'


class MagazineDetailView(DetailView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine-detail.html'


class IssueDetailView(DetailView):
    queryset = Issue.objects.all()
    template_name = 'appearances/issue-detail.html'
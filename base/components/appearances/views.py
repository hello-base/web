from django.views.generic import (ListView, DetailView, TemplateView, 
    CreateView, UpdateView)
from django.core.urlresolvers import reverse_lazy

from .forms import ShowForm, EpisodeForm, MagazineForm, IssueForm
from .models import Show, Episode, Magazine, Issue


class ShowListView(ListView):
    queryset = Show.objects.all()
    template_name = 'appearances/show-list.html'


class ShowDetailView(DetailView):
    queryset = Show.objects.all()
    template_name = 'appearances/show-detail.html'


class ShowCreateView(CreateView):
    model = Show
    success_url = reverse_lazy('show-detail')
    form_class = ShowForm


class ShowUpdateView(UpdateView):
    model = Show
    success_url = reverse_lazy('show-detail')
    form_class = ShowForm


class EpisodeDetailView(DetailView):
    queryset = Episode.objects.all()
    template_name = 'appearances/episode-detail.html'


class EpisodeCreateView(CreateView):
    model = Episode
    success_url = reverse_lazy('episode-detail')
    form_class = EpisodeForm


class EpisodeUpdateView(UpdateView):
    model = Episode
    success_url = reverse_lazy('episode-detail')
    form_class = EpisodeForm


class MagazineListView(ListView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine-list.html'


class MagazineDetailView(DetailView):
    queryset = Magazine.objects.all()
    template_name = 'appearances/magazine-detail.html'


class MagazineCreateView(CreateView):
    model = Magazine
    success_url = reverse_lazy('magazine-detail')
    form_class = MagazineForm


class MagazineUpdateView(UpdateView):
    model = Magazine
    success_url = reverse_lazy('magazine-detail')
    form_class = MagazineForm


class IssueDetailView(DetailView):
    queryset = Issue.objects.all()
    template_name = 'appearances/issue-detail.html'


class IssueCreateView(CreateView):
    model = Issue
    success_url = reverse_lazy('issue-detail')
    form_class = IssueForm


class IssueUpdateView(UpdateView):
    model = Issue
    success_url = reverse_lazy('issue-detail')
    form_class = IssueForm
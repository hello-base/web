from django.views.generic import DetailView, ListView, TemplateView

from braces.views import PrefetchRelatedMixin, SelectRelatedMixin

from .models import Album, Single, Track


class AlbumBrowseView(ListView):
    queryset = Album.objects.all()
    template_name = 'merchandise/music/album_browse.html'


class AlbumDetailView(DetailView):
    queryset = Album.objects.all()
    template_name = 'merchandise/music/album_detail.html'


class MusicBrowseView(TemplateView):
    template_name = 'merchandise/music/music_browse.html'


class SingleBrowseView(ListView):
    queryset = Single.objects.all()
    template_name = 'merchandise/music/single_browse.html'


class SingleDetailView(DetailView):
    model = Single
    # prefetch_related = ['editions__order', 'editions__videos']
    template_name = 'merchandise/music/single_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SingleDetailView, self).get_context_data(**kwargs)
        context['editions'] = self.object.editions.prefetch_related('order', 'videos')
        return context


class TrackBrowseView(ListView):
    queryset = Track.objects.all()
    template_name = 'merchandise/music/track_browse.html'


class TrackDetailView(DetailView):
    queryset = Track.objects.all()
    template_name = 'merchandise/music/track_detail.html'

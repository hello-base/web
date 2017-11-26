from django.views.generic import DetailView

from .models import Album, Single, Track


class AlbumDetailView(DetailView):
    queryset = Album.objects.all()
    template_name = 'merchandise/music/album_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['editions'] = self.object.editions.prefetch_related('order', 'videos')
        context['fact'] = self.object.facts.order_by('?').first()
        context['idols'] = self.object.idols.order_by('birthdate')
        return context


class SingleDetailView(DetailView):
    model = Single
    template_name = 'merchandise/music/single_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SingleDetailView, self).get_context_data(**kwargs)
        context['editions'] = self.object.editions.prefetch_related('order', 'videos')
        context['fact'] = self.object.facts.order_by('?').first()
        context['idols'] = self.object.idols.order_by('birthdate')
        return context


class TrackDetailView(DetailView):
    queryset = Track.objects.originals()
    template_name = 'merchandise/music/track_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TrackDetailView, self).get_context_data(**kwargs)
        context['appearances'] = self.object.appears_on.original_only()
        return context


class TrackLyricsView(DetailView):
    queryset = Track.objects.originals()
    template_name = 'merchandise/music/track_lyrics.html'

from django.views.generic import DetailView, ListView, TemplateView

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
    queryset = Single.objects.all()
    template_name = 'merchandise/music/single_detail.html'


class TrackBrowseView(ListView):
    queryset = Track.objects.all()
    template_name = 'merchandise/music/track_browse.html'


class TrackDetailView(DetailView):
    queryset = Track.objects.all()
    template_name = 'merchandise/music/track_detail.html'

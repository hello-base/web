from django.views.generic import ListView, DetailView

from .models import Event, Venue


class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/event_list.html'


class EventDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_detail.html'


class EventGoodsDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_goods_detail.html'


class VenueListView(ListView):
    queryset = Venue.objects.all()
    template_name = 'events/venue_list.html'


class VenueDetailView(DetailView):
    queryset = Venue.objects.all()
    template_name = 'events/venue_detail.html'

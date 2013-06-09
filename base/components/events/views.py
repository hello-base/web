from django.views.generic import ListView, DetailView, TemplateView

from .models import Event, Venue


class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/event-list.html'


class EventDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event-detail.html'


class EventGoodsDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event-goods-detail.html'


class VenueListView(ListView):
    queryset = Venue.objects.all()
    template_name = 'events/venue-list.html'


class VenueDetailView(DetailView):
    queryset = Venue.objects.all()
    template_name = 'events/venue-detail.html'
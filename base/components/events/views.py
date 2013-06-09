from django.views.generic import (ListView, DetailView, TemplateView, 
   CreateView, UpdateView)
from django.core.urlresolvers import reverse_lazy

from .forms import EventForm, VenueForm
from .models import Event, Venue


class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/event-list.html'


class EventDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event-detail.html'


class EventCreateView(CreateView):
    model = Event
    success_url = reverse_lazy('event-detail')
    form_class = EventForm


class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event-detail')
    form_class = EventForm


class EventGoodsDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event-goods-detail.html'


class VenueListView(ListView):
    queryset = Venue.objects.all()
    template_name = 'events/venue-list.html'


class VenueDetailView(DetailView):
    queryset = Venue.objects.all()
    template_name = 'events/venue-detail.html'


class VenueCreateView(CreateView):
    model = Venue
    success_url = reverse_lazy('venue-detail')
    form_class = VenueForm


class VenueUpdateView(UpdateView):
    model = Venue
    success_url = reverse_lazy('venue-detail')
    form_class = VenueForm
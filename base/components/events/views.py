from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from .forms import EventForm, PerformanceFormset, VenueForm
from .models import Event, Venue


class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/event_list.html'


class EventDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_detail.html'


class EventCreateView(CreateView):
    model = Event
    success_url = reverse_lazy('event-detail')
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['formset'] = PerformanceFormset()
        if self.request.POST:
            context['formset'] = PerformanceFormset(self.request.POST)
        return context


class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event-detail')
    form_class = EventForm


class EventGoodsDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_goods_detail.html'


class VenueListView(ListView):
    queryset = Venue.objects.all()
    template_name = 'events/venue_list.html'


class VenueDetailView(DetailView):
    queryset = Venue.objects.all()
    template_name = 'events/venue_detail.html'


class VenueCreateView(CreateView):
    model = Venue
    success_url = reverse_lazy('venue-detail')
    form_class = VenueForm


class VenueUpdateView(UpdateView):
    model = Venue
    success_url = reverse_lazy('venue-detail')
    form_class = VenueForm

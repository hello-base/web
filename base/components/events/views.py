from django.views.generic import ListView, DetailView, TemplateView

from .models import Event

class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/event-list.html'


class EventDetailView(DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event-detail.html'

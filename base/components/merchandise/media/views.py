from django.views.generic import DetailView

from .models import Videodisc


class VideodiscDetailView(DetailView):
    model = Videodisc
    template_name = 'merchandise/media/videodisc_detail.html'

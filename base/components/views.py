# -*- coding: utf-8 -*-
import datetime

from django.views.generic import TemplateView, View

from braces.views import AjaxResponseMixin, JSONResponseMixin
from haystack.query import SearchQuerySet

from components.correlations.models import Correlation
from components.merchandise.music.models import Album, Edition, Single, Track
from components.people.models import Group, Idol


class AutocompleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().autocomplete(text=query).load_all()[:5]
        suggestions = []
        [suggestions.append({
            'text': result.text,
            'pk': result.pk,
            'model': result.model_name,
            'name': result.object.name if result.object.name != result.object.romanized_name else None,
            'romanized_name': result.object.romanized_name,
            'url': result.object.get_absolute_url(),
        }) for result in sqs]
        json = {'query': query, 'results': suggestions}
        return self.render_json_response(json)


class SiteView(TemplateView):
    template_name = 'landings/site_home.html'

    def get_context_data(self, **kwargs):
        context = super(SiteView, self).get_context_data(**kwargs)
        correlations = Correlation.objects.prefetch_related('content_object')[:10]
        context['correlations'] = {
            'onthisday': Correlation.objects.prefetch_related('content_object').today(),
            'recent': [c for c in correlations if c.timestamp < datetime.date.today()],
            'today': [c for c in correlations if c.timestamp == datetime.date.today()],
            'upcoming': [c for c in correlations if c.timestamp > datetime.date.today()],
        }
        context['counts'] = {
            'albums': Album.objects.count(),
            'editions': Edition.objects.count(),
            'groups': Group.objects.count(),
            'idols': Idol.objects.count(),
            'singles': Single.objects.count(),
            'tracks': Track.objects.count(),
        }
        return context


class ImageDetailView(TemplateView):
    template_name = 'landings/image_detail.html'


class PlainTextView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TemplateView, self).render_to_response(context, content_type='text/plain', **kwargs)


class XMLView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TemplateView, self).render_to_response(context, content_type='application/opensearchdescription+xml', **kwargs)

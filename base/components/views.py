from django.views.generic import View
from django.views.generic.base import TemplateView

from braces.views import AjaxResponseMixin, JSONResponseMixin
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean


class AutocompleteView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().autocomplete(text=query).load_all()[:5]
        suggestions = []
        for result in sqs:
            suggestions.append({
                'text': result.text,
                'pk': result.pk,
                'model': result.model_name,
                'name': result.object.name if result.object.name != result.object.romanized_name else None,
                'romanized_name': result.object.romanized_name,
                'url': result.object.get_absolute_url(),
            })
        # suggestions = [result.pk for result in sqs]
        json = {'query': query, 'results': suggestions}
        return self.render_json_response(json)


class SiteView(TemplateView):
    template_name = 'landings/home_site.html'


class PlainTextView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TemplateView, self).render_to_response(context, content_type='text/plain', **kwargs)

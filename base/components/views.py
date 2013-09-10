from django.views.generic import View
from django.views.generic.base import TemplateView

from braces.views import AjaxResponseMixin, JSONResponseMixin
from haystack.query import SearchQuerySet


class SiteView(TemplateView):
    template_name = 'landings/home_site.html'


class AutocompleteView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        sqs = SearchQuerySet().autocomplete(text=request.GET.get('q', ''))[:5]
        suggestions = [result.pk for result in sqs]
        json = {'results': suggestions}
        return self.render_json_response(json)

from django.views.generic.base import TemplateView


class SiteView(TemplateView):
    template_name = 'landings/home_site.html'

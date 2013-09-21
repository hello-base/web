from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from components.views import AutocompleteView, PlainTextView, SiteView


# Administration system auto-discovery.
admin.autodiscover()

# Sitemaps, because Google.
sitemaps = {}

# The switch to faceted search requires a custom SearchQuerySet.
# By default we facet on "model" so the types of results can be
# displayed on the search results page.
sqs = SearchQuerySet().facet('model')

urlpatterns = patterns('',
    url(r'^$', name='site-home', view=SiteView.as_view()),
    url(r'^search/autocomplete/$', view=AutocompleteView.as_view()),
    url(r'^search/', name='search', view=FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs)),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Core Modules
    url(r'^accounts/', include('components.accounts.urls')),
    url(r'^', include('components.appearances.urls')),
    url(r'^', include('components.events.urls')),
    url(r'^', include('components.merchandise.goods.urls')),
    url(r'^', include('components.merchandise.music.urls')),
    url(r'^', include('components.people.urls')),

    # Sitemaps, Favicons, Robots, and Humans
    url(r'^favicon\.ico$', name='favicon', view=RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
    url(r'^humans.txt$', name='humans', view=PlainTextView.as_view(template_name='humans.txt')),
    url(r'^robots.txt$', name='robots', view=PlainTextView.as_view(template_name='robots.txt')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

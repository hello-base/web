# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from apps.sitemaps import (AlbumSitemap, IdolSitemap, GroupSitemap,
    SingleSitemap, TrackSitemap)
from apps.views import (AutocompleteView, ImageDetailView, PlainTextView,
    SiteView, WikiRedirectView, XMLView)


# Sitemaps, because Google.
sitemaps = {
    'albums': AlbumSitemap,
    'groups': GroupSitemap,
    'idols': IdolSitemap,
    'singles': SingleSitemap,
    'tracks': TrackSitemap
}

# The switch to faceted search requires a custom SearchQuerySet.
# By default we facet on "model" so the types of results can be
# displayed on the search results page.
sqs = SearchQuerySet().facet('model')

urlpatterns = [
    # Home and Search.
    url(r'^$', name='site-home', view=SiteView.as_view()),
    url(r'^search/autocomplete/$', name='autocomplete', view=AutocompleteView.as_view()),
    url(r'^search/', name='search', view=FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs)),

    # Imagery.
    url(r'^image/(?P<slug>([a-zA-Z\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif)))/$', name='image-detail', view=ImageDetailView.as_view()),

    # "Flatpages."
    url(r'^404/$', name='404', view=TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', name='500', view=TemplateView.as_view(template_name='500.html')),
    url(r'^about/$', name='about', view=TemplateView.as_view(template_name='landings/about.html')),
    url(r'^privacy/$', name='privacy', view=TemplateView.as_view(template_name='landings/privacy.html')),
    url(r'^terms/$', name='terms', view=TemplateView.as_view(template_name='landings/terms.html')),

    # J-Ongaku URL Override.
    url(r'^wiki/.*$', name='wiki-override', view=WikiRedirectView.as_view()),

    # Administration Modules.
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Authentication aliases.
    url(r'^signin/$', name='signin', view=RedirectView.as_view(url=reverse_lazy('oauth-authorize'), permanent=True)),

    # Core Modules.
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^', include('apps.appearances.urls')),
    url(r'^', include('apps.correlations.urls')),
    url(r'^', include('apps.events.urls')),
    url(r'^', include('apps.merchandise.goods.urls')),
    url(r'^', include('apps.merchandise.media.urls')),
    url(r'^', include('apps.merchandise.music.urls')),
    url(r'^', include('apps.news.urls')),
    url(r'^', include('apps.people.urls')),

    # Sitemaps, Favicons, Robots, and Humans.
    url(r'^favicon.ico$', name='favicon', view=RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico', permanent=True)),
    url(r'^humans.txt$', name='humans', view=PlainTextView.as_view(template_name='humans.txt')),
    url(r'^opensearch.xml$', name='opensearch', view=XMLView.as_view(template_name='opensearch.xml')),
    url(r'^robots.txt$', name='robots', view=PlainTextView.as_view(template_name='robots.txt')),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
]

# Since this module will only be called at startup, initialize our
# Segment.io analytics library here.
import analytics
analytics.write_key = 'qs70qk1'

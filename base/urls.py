# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, re_path, reverse_lazy
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic import RedirectView, TemplateView

# TEMPORARILY DISABLED - Haystack/search will be rebuilt
# from haystack.forms import FacetedSearchForm
# from haystack.query import SearchQuerySet
# from haystack.views import FacetedSearchView

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

# TEMPORARILY DISABLED - Search will be rebuilt
# sqs = SearchQuerySet().facet('model')

urlpatterns = [
    # Home and Search.
    re_path(r'^$', SiteView.as_view(), name='site-home'),
    re_path(r'^search/autocomplete/$', AutocompleteView.as_view(), name='autocomplete'),
    # TEMPORARILY DISABLED - Search will be rebuilt
    # re_path(r'^search/', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='search'),
    re_path(r'^search/$', TemplateView.as_view(template_name='search/search.html'), name='search'),

    # Imagery.
    re_path(r'^image/(?P<slug>([a-zA-Z\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif)))/$', ImageDetailView.as_view(), name='image-detail'),

    # "Flatpages."
    re_path(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
    re_path(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    re_path(r'^about/$', TemplateView.as_view(template_name='landings/about.html'), name='about'),
    re_path(r'^privacy/$', TemplateView.as_view(template_name='landings/privacy.html'), name='privacy'),
    re_path(r'^terms/$', TemplateView.as_view(template_name='landings/terms.html'), name='terms'),

    # J-Ongaku URL Override.
    re_path(r'^wiki/.*$', WikiRedirectView.as_view(), name='wiki-override'),

    # Administration Modules.
    re_path(r'^grappelli/', include('grappelli.urls')),
    re_path(r'^admin/', admin.site.urls),

    # Authentication aliases.
    re_path(r'^signin/$', RedirectView.as_view(url=reverse_lazy('oauth-authorize'), permanent=True), name='signin'),

    # Core Modules.
    re_path(r'^accounts/', include('apps.accounts.urls')),
    re_path(r'^', include('apps.appearances.urls')),
    re_path(r'^', include('apps.correlations.urls')),
    re_path(r'^', include('apps.events.urls')),
    re_path(r'^', include('apps.merchandise.goods.urls')),
    re_path(r'^', include('apps.merchandise.media.urls')),
    re_path(r'^', include('apps.merchandise.music.urls')),
    re_path(r'^', include('apps.news.urls')),
    re_path(r'^', include('apps.people.urls')),

    # Sitemaps, Favicons, Robots, and Humans.
    re_path(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico', permanent=True), name='favicon'),
    re_path(r'^humans.txt$', PlainTextView.as_view(template_name='humans.txt'), name='humans'),
    re_path(r'^opensearch.xml$', XMLView.as_view(template_name='opensearch.xml'), name='opensearch'),
    re_path(r'^robots.txt$', PlainTextView.as_view(template_name='robots.txt'), name='robots'),
    re_path(r'^sitemap.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# TEMPORARILY DISABLED - Analytics initialization
# Since this module will only be called at startup, initialize our
# Segment.io analytics library here.
# import analytics
# analytics.write_key = 'qs70qk1'

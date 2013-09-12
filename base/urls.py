from django.conf.urls import patterns, include, url
from django.contrib import admin

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from components.views import AutocompleteView, SiteView

# Uncomment the next two lines to enable the admin:
# admin.autodiscover()

# The switch to faceted search requires a custom SearchQuerySet.
# By default we facet on "model" so the types of results can be
# displayed on the search results page.
sqs = SearchQuerySet().facet('model')

urlpatterns = patterns('',
    url(r'^$', name='site-home', view=SiteView.as_view()),
    url(r'^search/', name='search', view=FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs)),
    url(r'^search/autocomplete/$', view=AutocompleteView.as_view()),

    url(r'^', include('components.appearances.urls')),
    url(r'^', include('components.events.urls')),

    url(r'^', include('components.merchandise.goods.urls')),
    url(r'^', include('components.merchandise.music.urls')),
    url(r'^', include('components.people.urls')),

    # Examples:
    # url(r'^$', 'base.views.home', name='home'),
    # url(r'^base/', include('base.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

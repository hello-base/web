from django.conf.urls import patterns, include, url
from django.contrib import admin

from components.views import SiteView

# Uncomment the next two lines to enable the admin:
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', name='site-home', view=SiteView.as_view()),

    url(r'^', include('components.appearances.urls')),
    url(r'^', include('components.events.urls')),
    url(r'^', include('components.merchandise.goods.urls')),

    # Examples:
    # url(r'^$', 'base.views.home', name='home'),
    # url(r'^base/', include('base.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

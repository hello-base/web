from django.conf.urls import patterns, url

from .views import PreAuthorizationView, PostAuthorizationView


urlpatterns = patterns('',
    url(r'^authorize/$', name='oauth-authorize', view=PreAuthorizationView.as_view()),
    url(r'^authenticated/$', name='oauth-callback', view=PostAuthorizationView.as_view()),
)

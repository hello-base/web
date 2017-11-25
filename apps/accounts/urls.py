from django.conf.urls import url

from .views import PreAuthorizationView, PostAuthorizationView


urlpatterns = [
    url(r'^authorize/$', name='oauth-authorize', view=PreAuthorizationView.as_view(permanent=True)),
    url(r'^authenticated/$', name='oauth-callback', view=PostAuthorizationView.as_view()),
]

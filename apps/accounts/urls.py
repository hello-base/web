from django.urls import re_path

from .views import PreAuthorizationView, PostAuthorizationView


urlpatterns = [
    re_path(r'^authorize/$', PreAuthorizationView.as_view(permanent=True), name='oauth-authorize'),
    re_path(r'^authenticated/$', PostAuthorizationView.as_view(), name='oauth-callback'),
]

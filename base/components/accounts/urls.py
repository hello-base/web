from django.conf.urls import patterns, url

from .views import ProcessUserView


urlpatterns = patterns('',
    url(r'^accounts/authenticated/$', name='authenticated-user', view=ProcessUserView),
)

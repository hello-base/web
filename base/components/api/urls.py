from django.conf.urls import patterns, url, include

from .views import GroupList, IdolList


group_urls = patterns('',
    url(r'^$', GroupList.as_view(), name='group-list'),
)

idol_urls = patterns('',
    url(r'^$', IdolList.as_view(), name='idol-list'),
)

urlpatterns = patterns('',
    url(r'^groups', include(group_urls)),
    url(r'^idols', include(idol_urls)),
)

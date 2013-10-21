from django.conf.urls import patterns, url, include

from .views import (GroupList, GroupDetail, GroupMembershipsList,
    GroupActiveMembershipsList, GroupInactiveMembershipsList)
from .views import IdolList, IdolDetail


group_urls = patterns('',
    url(r'^/(?P<slug>[-\w]+)/members$', name='group-members', view=GroupMembershipsList.as_view()),
    url(r'^/(?P<slug>[-\w]+)/members/active$', name='group-members-active', view=GroupActiveMembershipsList.as_view()),
    url(r'^/(?P<slug>[-\w]+)/members/inactive$', name='group-members-inactive', view=GroupInactiveMembershipsList.as_view()),
    url(r'^/(?P<slug>[-\w]+)$', name='group-detail', view=GroupDetail.as_view()),
    url(r'^$', name='group-list', view=GroupList.as_view()),
)

idol_urls = patterns('',
    url(r'^/(?P<slug>[-\w]+)$', name='idol-detail', view=IdolDetail.as_view()),
    url(r'^$', name='idol-list', view=IdolList.as_view()),
)

urlpatterns = patterns('',
    url(r'^groups', include(group_urls)),
    url(r'^idols', include(idol_urls)),
)

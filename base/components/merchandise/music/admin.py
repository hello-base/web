from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import (Album, Edition, Label, Single, Track, TrackOrder,
    Video, VideoTrackOrder)


admin.site.register(Album)
admin.site.register(Single)

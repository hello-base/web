from django.contrib import admin

from .models import Channel, Thumbnail, Video


class VideoInline(admin.StackedInline):
    extra = 1
    model = Video


class ThumbnailInline(admin.TabularInline):
    extra = 1
    model = Thumbnail


class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Relations', {'fields': ('idol', 'group')}),
    )
    inlines = [VideoInline]
    list_display = ['username', 'idol', 'group']
    list_select_related = True

    raw_id_fields = ('idol', 'group',)
    autocomplete_lookup_fields = {'fk': ['idol', 'group']}
admin.site.register(Channel, ChannelAdmin)


class VideoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('channel', 'ytid')}),
        (None, {'fields': ('title', 'description', 'published', 'duration')}),
    )
    inlines = [ThumbnailInline]
    list_display = ['title', 'channel', 'published', 'duration', 'ytid']
    list_select_related = True

    raw_id_fields = ('channel',)
    autocomplete_lookup_fields = {'fk': ['channel']}
admin.site.register(Video, VideoAdmin)

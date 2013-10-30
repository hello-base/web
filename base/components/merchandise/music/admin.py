from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import (Album, Edition, Label, Single, Track, TrackOrder,
    Video, VideoTrackOrder)


class AlbumEditionInline(admin.StackedInline):
    exclude = ['single']
    extra = 1
    fieldsets = ((None, {'fields': ('kind', 'released', ('romanized_name', 'name'), ('catalog_number', 'price'), 'art')}),)
    model = Edition


class SingleEditionInline(admin.StackedInline):
    exclude = ['album']
    extra = 1
    fieldsets = ((None, {'fields': ('kind', 'released', ('romanized_name', 'name'), ('catalog_number', 'price'), 'art')}),)
    model = Edition


class TrackOrderInline(admin.TabularInline):
    extra = 1
    fieldsets = ((None, {'fields': ('track', 'position', 'is_aside', 'is_bside', 'is_instrumental', 'is_album_only')}),)
    model = TrackOrder
    verbose_name_plural = 'Track Order'

    raw_id_fields = ['track']
    autocomplete_lookup_fields = {'fk': ['track']}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TrackOrderInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'track':
            formfield.choices = formfield.choices
        return formfield


class VideoTrackOrderInline(admin.TabularInline):
    extra = 1
    model = VideoTrackOrder
    verbose_name_plural = 'Video Track Order'

    raw_id_fields = ['video']
    autocomplete_lookup_fields = {'fk': ['video']}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(VideoTrackOrderInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'video':
            formfield.choices = formfield.choices
        return formfield


class LabelAdmin(admin.ModelAdmin):
    pass
admin.site.register(Label, LabelAdmin)


class MusicBaseAdmin(admin.ModelAdmin):
    pass


class AlbumAdmin(ContributorMixin, MusicBaseAdmin):
    pass
admin.site.register(Album, AlbumAdmin)


class SingleAdmin(ContributorMixin, MusicBaseAdmin):
    pass
admin.site.register(Single, SingleAdmin)


class EditionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Edition, EditionAdmin)


class TrackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Track, TrackAdmin)


class VideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Video, VideoAdmin)

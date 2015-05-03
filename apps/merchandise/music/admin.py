# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from markdown import markdown

from django.contrib import admin

from apps.accounts.admin import ContributorMixin
from apps.merchandise.stores.admin import PurchaseLinkInline
from apps.prose.admin import FactInline

from .models import (Album, Edition, Label, Single, Track, TrackOrder, Video,
    VideoTrackOrder)


class ReleaseEditionInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': ('kind', 'released', ('romanized_name', 'name'), ('catalog_number', 'price'), 'art')}),)
    model = Edition


class AlbumEditionInline(ReleaseEditionInline):
    exclude = ['single']


class SingleEditionInline(ReleaseEditionInline):
    exclude = ['album']


class TrackOrderInline(admin.TabularInline):
    extra = 1
    fieldsets = ((None, {'fields': ('track', 'disc', 'position', 'is_aside', 'is_bside', 'is_instrumental', 'is_album_only')}),)
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
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'slug', 'logo')}),)
    list_display = ['romanized_name', 'name', 'slug']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
admin.site.register(Label, LabelAdmin)


class MusicBaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'released'
    filter_horizontal = ['idols', 'groups']
    list_display = ['romanized_name', 'name', 'released', 'label', 'participant_list', 'number', 'romanized_released_as']
    list_editable = ['released', 'label']
    list_select_related = True
    ordering = ('-modified',)
    prepopulated_fields = {'slug': ['romanized_name']}
    readonly_fields = ['participating_groups', 'participating_idols', 'released', 'art']
    search_fields = ['romanized_name', 'name', 'idols__name', 'idols__romanized_family_name', 'idols__romanized_given_name', 'groups__name', 'groups__romanized_name']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}

    def save_related(self, request, form, formsets, change):
        super(MusicBaseAdmin, self).save_related(request, form, formsets, change)
        form.instance.save()

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs['request']
        formfield = super(MusicBaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'label':
            label_choices_cache = getattr(request, 'label_choices_cache', None)
            if label_choices_cache is not None:
                formfield.choices = label_choices_cache
            else:
                request.label_choices_cache = formfield.choices
        return formfield

    def participant_list(self, obj):
        return ', '.join([p.romanized_name for p in obj.participants])
    participant_list.short_description = 'Participant List'


class AlbumAdmin(ContributorMixin, MusicBaseAdmin):
    fieldsets = (
        (None, {'fields': ('number', ('romanized_name', 'name'), 'slug', 'label')}),
        (None, {
            'description': 'These are derived from this release\'s regular edition. Please change those fields to change this one.',
            'fields': ('released', 'art')
        }),
        ('Participants', {'fields': (('romanized_released_as', 'released_as'), 'idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Alternates', {'fields': ('is_indie', 'is_compilation')}),
        ('Internal Notes', {'fields': ('note',)}),
    )
    inlines = [AlbumEditionInline, FactInline, PurchaseLinkInline]
admin.site.register(Album, AlbumAdmin)


class SingleAdmin(ContributorMixin, MusicBaseAdmin):
    fieldsets = (
        (None, {'fields': ('number', ('romanized_name', 'name'), 'slug', 'label')}),
        (None, {
            'description': 'These are derived from this release\'s regular edition. Please change those fields to change this one.',
            'fields': ('released', 'art'),
        }),
        ('Participants', {'fields': (('romanized_released_as', 'released_as'), 'idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Alternates', {
            'classes': ('collapse closed',),
            'fields': ('is_indie', ('has_8cm', 'has_lp', 'has_cassette'))
        }),
        ('Internal Notes', {'fields': ('note',)}),
    )
    inlines = [SingleEditionInline, FactInline, PurchaseLinkInline]
admin.site.register(Single, SingleAdmin)


class EditionAdmin(admin.ModelAdmin):
    date_hierarchy = 'released'
    fieldsets = (
        (None, {'fields': ('kind',)}),
        ('Relations', {'fields': ('album', 'single')}),
        ('Content', {'fields': ('romanized_name', 'released', 'catalog_number', 'price', 'art')})
    )
    inlines = [TrackOrderInline, VideoTrackOrderInline]
    list_display = ['__unicode__', 'kind', 'romanized_name', 'name', 'released', 'catalog_number']
    list_display_links = ['__unicode__', 'kind']
    list_filter = ['kind']
    list_select_related = True
    ordering = ('-released',)
    search_fields = [
        'album__romanized_name', 'album__name',
        'single__romanized_name', 'single__name',
        'romanized_name', 'name',
    ]

    raw_id_fields = ('album', 'single',)
    autocomplete_lookup_fields = {'fk': ['album', 'single']}
admin.site.register(Edition, EditionAdmin)


class TrackAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('romanized_name', 'name'), 'slug',)}),
        ('Relations', {
            'description': 'Only enter the release which this track <b>first appeared on</b>.',
            'fields': ('album', 'single')
        }),
        ('Participants', {
            'description': 'Enter all the idols and groups that participated. Only add a group if <b>all</b> of its members participated.',
            'fields': (('romanized_released_as', 'released_as'), 'idols', 'groups')
        }),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Alternates', {'fields': ('original_track', 'is_cover', 'is_alternate', ('romanized_name_alternate', 'name_alternate'))}),
        ('Staff Involved', {
            'description': 'For reference: lyricist = <b>作詞</b>, composer = <b>作曲</b>, arranger = <b>編曲</b>.',
            'fields': ('lyricists', 'composers', 'arrangers')
        }),
        ('Lyrics', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('translated_name', 'lyrics', 'romanized_lyrics', 'translated_lyrics', 'translation_notes')
        }),
        ('Internal Notes', {'fields': ('note',)}),
    )
    filter_horizontal = ['idols', 'groups', 'arrangers', 'composers', 'lyricists']
    list_display = ['__unicode__', 'name', 'is_cover', 'is_alternate', 'original_track', 'romanized_name_alternate', 'name_alternate', 'participant_list']
    list_display_links = ['__unicode__', 'name']
    list_filter = ['is_cover', 'is_alternate']
    list_select_related = True
    ordering = ('-id',)
    prepopulated_fields = {'slug': ['romanized_name']}
    readonly_fields = ['participating_groups', 'participating_idols']
    search_fields = [
        'idols__romanized_name', 'idols__romanized_family_name', 'idols__romanized_given_name',
        'groups__romanized_name', 'groups__name',
        'romanized_name', 'name', 'is_alternate', 'romanized_name_alternate', 'name_alternate', 'slug'
    ]

    raw_id_fields = ('album', 'single', 'idols', 'groups', 'original_track', 'arrangers', 'composers', 'lyricists')
    autocomplete_lookup_fields = {
        'fk': ['album', 'single', 'original_track'],
        'm2m': ['idols', 'groups', 'arrangers', 'composers', 'lyricists']
    }

    def save_model(self, request, obj, form, change):
        extensions = ['nl2br', 'apps.extensions.markdown.lyriccoding']
        obj.processed_lyrics = markdown(obj.lyrics, extensions)
        obj.processed_romanized_lyrics = markdown(obj.romanized_lyrics, extensions)
        obj.processed_translated_lyrics = markdown(obj.translated_lyrics, extensions)
        obj.save()

    def participant_list(self, obj):
        return ', '.join([p.romanized_name for p in obj.participants])
    participant_list.short_description = 'Participant List'
admin.site.register(Track, TrackAdmin)


class VideoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('kind',)}),
        (None, {'fields': (('romanized_name', 'name'),)}),
        ('Relations', {'fields': ('album', 'single')})
    )
    list_display = ['romanized_name', 'name', 'kind', 'released', 'video_url']
    list_editable = ['kind']
    list_filter = ['kind']
    ordering = ('-id',)
    search_fields = ['romanized_name']

    raw_id_fields = ('album', 'single',)
    autocomplete_lookup_fields = {'fk': ['album', 'single']}
admin.site.register(Video, VideoAdmin)

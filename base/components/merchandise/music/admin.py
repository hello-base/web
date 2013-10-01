from django.contrib import admin

from .models import (Album, Edition, Label, Single, Track, TrackOrder,
    Video, VideoTrackOrder)


class AlbumEditionInline(admin.StackedInline):
    exclude = ['single']
    extra = 1
    fieldsets = (
        (None, {'fields': ('kind', 'released', ('romanized_name', 'name'), 'catalog_number', 'art')}),
    )
    model = Edition


class SingleEditionInline(admin.StackedInline):
    exclude = ['album']
    extra = 1
    fieldsets = (
        (None, {'fields': ('kind', 'released', ('romanized_name', 'name'), 'catalog_number', 'art')}),
    )
    model = Edition


class TrackOrderInline(admin.TabularInline):
    extra = 1
    model = TrackOrder
    verbose_name_plural = 'Track Order'

    raw_id_fields = ['track']
    autocomplete_lookup_fields = {'fk': ['track']}


class VideoTrackOrderInline(admin.TabularInline):
    extra = 1
    model = VideoTrackOrder
    verbose_name_plural = 'Video Track Order'

    raw_id_fields = ['video']
    autocomplete_lookup_fields = {'fk': ['video']}


class MusicBaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'released'
    filter_horizontal = ['idols', 'groups']
    list_select_related = True
    ordering = ('-modified',)
    search_fields = ['romanized_name', 'name', 'idols__name', 'idols__family_kanji', 'idols__given_kanji', 'groups__name', 'groups__kanji']
    prepopulated_fields = {'slug': ['romanized_name']}


class AlbumAdmin(MusicBaseAdmin):
    fieldsets = (
        (None, {'fields': ('number', ('romanized_name', 'name'), 'slug')}),
        (None, {
            'description': 'This is derived from this release\'s regular edition. Please change that date to change this one.',
            'fields': ('released',)}),
        ('Relations', {'fields': ('idols', 'groups')}),
        ('Alternates', {'fields': ('is_compilation',)})
    )
    inlines = [AlbumEditionInline]
    list_display = ['romanized_name', 'name', 'number', 'released', 'participant_list', 'is_compilation']
    list_editable = ['number', 'released', 'is_compilation']
    readonly_fields = ['released']
    save_on_top = True

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}

    def participant_list(self, obj):
        return ', '.join([p.romanized_name for p in obj.participants])
    participant_list.short_description = 'Participant List'
admin.site.register(Album, AlbumAdmin)


class EditionAdmin(admin.ModelAdmin):
    date_hierarchy = 'released'
    fieldsets = (
        (None, {'fields': ('kind',)}),
        ('Relations', {'fields': ('album', 'single')}),
        ('Content', {'fields': ('romanized_name', 'released', 'catalog_number', 'price', 'art')})
    )
    inlines = [TrackOrderInline, VideoTrackOrderInline]
    list_display = ['parent', 'kind', 'romanized_name', 'released', 'catalog_number']
    list_display_links = ['parent', 'kind']
    list_filter = ['kind']
    list_select_related = True
    ordering = ('-modified',)
    save_on_top = True
    search_fields = ['album__name', 'single__name', 'album__idols__name', 'album__groups__name', 'single__idols__name', 'single__groups__name', 'romanized_name']

    raw_id_fields = ('album', 'single',)
    autocomplete_lookup_fields = {'fk': ['album', 'single']}
admin.site.register(Edition, EditionAdmin)


class LabelAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('name', 'slug')}),)
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
admin.site.register(Label, LabelAdmin)


class SingleAdmin(MusicBaseAdmin):
    fieldsets = (
        (None, {'fields': ('number', ('romanized_name', 'name'), 'slug')}),
        (None, {
            'description': 'This is derived from this release\'s regular edition. Please change that date to change this one.',
            'fields': ('released',)
        }),
        ('Relations', {'fields': ('idols', 'groups')}),
        ('Alternates', {
            'classes': ('collapse closed',),
            'fields': ('is_indie', 'has_8cm', 'has_lp', 'has_cassette')
        })
    )
    inlines = [SingleEditionInline]
    list_display = ['romanized_name', 'name', 'number', 'released', 'participant_list']
    list_editable = ['number', 'released']
    readonly_fields = ['released']
    save_on_top = True

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}

    def participant_list(self, obj):
        return ', '.join([p.romanized_name for p in obj.participants])
    participant_list.short_description = 'Participant List'
admin.site.register(Single, SingleAdmin)


class TrackAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('romanized_name', 'name')}),
        ('Relations', {'fields': ('idols', 'groups')}),
        ('Alternates', {
            'classes': ('collapse closed',),
            'fields': ('original_track', 'is_cover', 'is_alternate', 'romanized_name_alternate', 'name_alternate')
        }),
        ('Staff Involved', {
            'classes': ('collapse closed',),
            'fields': ('arrangers', 'composers', 'lyricists')
        })
    )
    filter_horizontal = ['idols', 'groups', 'arrangers', 'composers', 'lyricists']
    list_display = ['romanized_name', 'name', 'is_cover', 'is_alternate', 'romanized_name_alternate', 'name_alternate']
    list_display_links = ['romanized_name', 'name']
    list_filter = ['is_alternate']
    list_select_related = True
    ordering = ('-modified',)
    save_on_top = True
    search_fields = ['romanized_name', 'name', 'idols__romanized_name', 'idols__romanized_family_name', 'idols__romanized_given_name', 'groups__romanized_name', 'groups__name', 'is_alternate', 'romanized_name_alternate', 'name_alternate']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'fk': ['original_track',], 'm2m': ['idols', 'groups']}
admin.site.register(Track, TrackAdmin)


class VideoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('kind',)}),
        (None, {'fields': ('romanized_name', 'name', 'released')}),
        ('Relations', {'fields': ('album', 'single')}),
        ('Details', {
            'classes': ('collapse closed',),
            'fields': ('still', 'video_url')
        })
    )
    list_display = ['romanized_name', 'name', 'kind', 'released', 'video_url']
    list_editable = ['kind']
    list_filter = ['kind']
    save_on_top = True
    search_fields = ['romanized_name']

    raw_id_fields = ('album', 'single',)
    autocomplete_lookup_fields = {'fk': ['album', 'single']}
admin.site.register(Video, VideoAdmin)

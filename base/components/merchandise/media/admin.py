# -*- coding: utf-8 -*-
from django.contrib import admin

from components.accounts.admin import ContributorMixin
from .models import Clip, Videodisc, VideodiscFormat


class ClipInline(admin.StackedInline):
    extra = 1
    fieldsets = (
        (None, {'fields': (('disc', 'position'), 'track', ('romanized_name', 'name'))}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
    )
    model = Clip
    readonly_fields = ['participating_groups', 'participating_idols']

    raw_id_fields = ('idols', 'groups', 'track',)
    autocomplete_lookup_fields = {
        'fk': ['track'],
        'm2m': ['idols', 'groups']
    }


class VideodiscFormatInline(admin.TabularInline):
    extra = 1
    model = VideodiscFormat


class VideodiscFormatAdmin(admin.ModelAdmin):
    date_hierarchy = 'released'
    fieldsets = (
        (None, {'fields': ('kind',)}),
        ('Relations', {'fields': ('parent',)}),
        ('Content', {'fields': ('released', 'catalog_number', 'art')})
    )
    inlines = [ClipInline]
    list_display = ['parent', 'kind', 'released', 'catalog_number']
    list_display_links = ['parent', 'kind']
    list_filter = ['kind']
    list_select_related = True
    search_fields = ['parent__romanized_name', 'parent__name', 'catalog_number']
admin.site.register(VideodiscFormat, VideodiscFormatAdmin)


class VideodiscAdmin(ContributorMixin):
    date_hierarchy = 'released'
    fieldsets = (
        (None, {'fields': ('kind',)}),
        ('Basics', {'fields': (('romanized_name', 'name'),)}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
    )
    inlines = [VideodiscFormatInline]
    list_display = ['romanized_name', 'name', 'released', 'kind']
    list_editable = ['kind']
    readonly_fields = ['participating_groups', 'participating_idols']
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}
admin.site.register(Videodisc, VideodiscAdmin)

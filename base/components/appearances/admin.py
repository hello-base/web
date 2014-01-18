# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (Card, CardSet, Episode, Issue, IssueImage, Magazine,
    Show, Summary, TimeSlot)


class SummaryInline(admin.StackedInline):
    extra = 1
    fields = ['body', 'submitted_by']
    model = Summary

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'submitted_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(SummaryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TimeSlotInline(admin.TabularInline):
    extra = 1
    model = TimeSlot


class ShowAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': (('romanized_name', 'name'), 'slug', 'description', ('aired_from', 'aired_until'))}),
    )
    list_display = ['romanized_name', 'name', 'aired_from', 'aired_until']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}

    inlines = [TimeSlotInline]
admin.site.register(Show, ShowAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': ('show', ('romanized_name', 'name'), ('air_date', 'record_date', 'number'), 'video_link')}),
        (None, {
            'description': 'If this is a continuation of another episode, enter that episode below.',
            'fields': ('episode',)
        }),
        ('Participants', {
            'description': 'Enter <i>every</i> idol and all groups that participated in this event.',
            'fields': ('idols', 'groups')
        }),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
    )
    inlines = [SummaryInline]
    list_display = ['show', 'air_date', 'romanized_name', 'name']
    readonly_fields = ['participating_groups', 'participating_idols']

    raw_id_fields = ['show', 'episode', 'idols', 'groups']
    autocomplete_lookup_fields = {
        'fk': ['show', 'episode'],
        'm2m': ['idols', 'groups']
    }
admin.site.register(Episode, EpisodeAdmin)


class IssueInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': ('release_date', 'volume_number', ('catalog_number', 'isbn_number'), 'cover')}),)
    model = Issue


class IssueImageInline(admin.TabularInline):
    extra = 1
    model = IssueImage


class MagazineAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': (('romanized_name', 'name'), 'slug', 'price')}),
    )
    inlines = [IssueInline]
    list_display = ['romanized_name', 'name', 'price']
    list_display_links = ['romanized_name', 'name']
admin.site.register(Magazine, MagazineAdmin)


class IssueAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': ('magazine', 'release_date', 'volume_number', ('catalog_number', 'isbn_number'), 'cover')}),
        ('Participants', {
            'description': 'Enter <i>every</i> idol and all groups that participated in this event.',
            'fields': ('idols', 'groups')
        }),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
    )
    inlines = [IssueImageInline, SummaryInline]
    list_display = ['magazine', 'volume_number', 'release_date', 'catalog_number', 'isbn_number']
    list_display_links = ['magazine', 'volume_number']
    readonly_fields = ['participating_groups', 'participating_idols']

    raw_id_fields = ['magazine', 'idols', 'groups']
    autocomplete_lookup_fields = {
        'fk': ['magazine'],
        'm2m': ['idols', 'groups']
    }
admin.site.register(Issue, IssueAdmin)


class CardInline(admin.StackedInline):
    extra = 1
    fieldsets = (
        (None, {'fields': ('issue', 'number', 'image')}),
        ('H!P Information', {'fields': ('hp_model', 'member_of', 'group')}),
        ('Non-H!P Information', {
            'classes': ('grp-collapse grp-closed',),
            'fields': (('other_model_romanized_name', 'other_model_name'), ('other_member_of_romanized_name', 'other_member_of_name'), ('other_group_romanized_name', 'other_group_name'))
        }),
    )
    model = Card

    raw_id_fields = ['issue', 'hp_model', 'member_of', 'group']
    autocomplete_lookup_fields = {'fk': ['issue', 'hp_model', 'member_of', 'group']}


class CardSetAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': ('issue', 'romanized_name', 'image')}),
    )
    inlines = [CardInline]
    list_display = ['issue', 'romanized_name']

    raw_id_fields = ['issue']
    autocomplete_lookup_fields = {'fk': ['issue']}
admin.site.register(CardSet, CardSetAdmin)

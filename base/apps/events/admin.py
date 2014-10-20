# -*- coding: utf-8 -*-
from django.contrib import admin

from base.apps.accounts.admin import ContributorMixin
from base.apps.prose.admin import FactInline, SummaryInline

from .models import Activity, Event, Venue


class ActivityInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'venue', 'venue_known_as', ('day', 'start_time'), 'is_performance')}),)
    model = Activity

    raw_id_fields = ('venue',)
    autocomplete_lookup_fields = {'fk': ['venue']}


class EventAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Basics', {'fields': ('category', ('has_handshake', 'is_fanclub', 'is_international'),)}),
        ('Dates', {'fields': (('start_date', 'end_date'),)}),
        ('Names', {'fields': (('romanized_name', 'name'), 'nickname', 'slug')}),
        ('Participants', {
            'description': 'Enter <i>every</i> idol and all groups that participated in this event.',
            'fields': ('idols', 'groups')
        }),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Links', {'fields': ('info_link_name', 'info_link')}),
        ('Imagery', {'fields': ('logo', 'promotional_image', 'stage')}),
    )
    inlines = [ActivityInline, FactInline, SummaryInline]
    list_display = ['romanized_name', 'name', 'nickname', 'start_date', 'end_date']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    readonly_fields = ['participating_groups', 'participating_idols']
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}
admin.site.register(Event, EventAdmin)


class ActivityAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'day'
    fieldsets = (
        (None, {'fields': ('event', 'venue', 'venue_known_as')}),
        ('Dates', {'fields': (('day', 'start_time'),)}),
        ('Details', {'fields': (('romanized_name', 'name'), 'is_performance')}),
    )
    inlines = [FactInline, SummaryInline]
    list_display = ['event', 'day', 'start_time', 'romanized_name', 'name', 'venue']
    list_display_links = ['event', 'day']
    list_select_related = True
    search_fields = ['day', 'start_time', 'event', 'venue']

    raw_id_fields = ('event', 'venue')
    autocomplete_lookup_fields = {'fk': ['event', 'venue']}
admin.site.register(Activity, ActivityAdmin)


class VenueAdmin(ContributorMixin, admin.ModelAdmin):
    fieldsets = (
        ('Names', {'fields': (('romanized_name', 'name'), 'other_names', 'slug')}),
        ('Details', {'fields': ('capacity', 'url', 'photo')}),
        ('Location', {'fields': ('romanized_address', 'address', 'country')}),
    )
    list_display = ['romanized_name', 'name', 'other_names', 'romanized_address', 'country']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    search_fields = ['romanized_name', 'name', 'country']
admin.site.register(Venue, VenueAdmin)

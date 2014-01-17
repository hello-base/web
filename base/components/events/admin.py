# -*- coding: utf-8 -*-
from django.contrib import admin

from components.accounts.admin import ContributorMixin
from components.facts.admin import FactInline

from .models import Event, Performance, Venue


class PerformanceInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'venue', 'venue_known_as', ('day', 'start_time'))}),)
    model = Performance

    raw_id_fields = ('venue',)
    autocomplete_lookup_fields = {'fk': ['venue']}


class SummaryInline(admin.StackedInline):
    extra = 1
    fields = ['body', 'submitted_by']
    model = Summary

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'submitted_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(SummaryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class EventAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'start_date'
    fieldsets = (
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
        ('Links', {'fields': ('info_link', 'secondary_info_link')}),
        ('Imagery', {'fields': ('logo', 'poster', 'stage')}),
    )
    inlines = [PerformanceInline, FactInline, SummaryInline]
    list_display = ['romanized_name', 'name', 'nickname', 'start_date', 'end_date']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    readonly_fields = ['participating_groups', 'participating_idols']
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'day'
    fieldsets = (
        (None, {'fields': ('event', 'venue', 'venue_known_as')}),
        ('Dates', {'fields': (('day', 'start_time'),)}),
        ('Details', {'fields': (('romanized_name', 'name'),)}),
    )
    inlines = [FactInline]
    list_display = ['event', 'day', 'start_time', 'romanized_name', 'name', 'venue']
    list_display_links = ['event', 'day']
    list_select_related = True
    search_fields = ['day', 'start_time', 'event', 'venue']

    raw_id_fields = ('event', 'venue')
    autocomplete_lookup_fields = {'fk': ['event', 'venue']}
admin.site.register(Performance, PerformanceAdmin)


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

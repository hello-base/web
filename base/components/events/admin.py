from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import Event, Performance, Venue


class PerformanceInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'venue', 'venue_known_as', ('day', 'start_time'))}),)
    model = Performance

    raw_id_fields = ('venue',)
    autocomplete_lookup_fields = {'fk': ['venue']}


class EventAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Dates', {'fields': (('start_date', 'end_date'),)}),
        ('Names', {'fields': (('romanized_name', 'name'), 'nickname', 'slug')}),
        ('Relations', {
            'description': 'Enter <i>every</i> idol and all groups that participated in this event.',
            'fields': ('idols', 'groups')
        }),
        ('Links', {'fields': ('info_link', 'secondary_info_link')}),
        ('Imagery', {'fields': ('logo', 'poster', 'stage')}),
    )
    inlines = [PerformanceInline]
    list_display = ['romanized_name', 'name', 'nickname', 'start_date', 'end_date']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('idols', 'groups',)
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups']}
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'day'
    fieldsets = (
        (None, {'fields': ('event', 'venue', 'venue_known_as')}),
        ('Dates', {'fields': (('day', 'start_time'),)}),
        ('Names', {'fields': (('romanized_name', 'name'),)}),
    )
    list_display = ['romanized_name', 'name', 'day', 'start_time', 'event', 'venue']
    list_display_links = ['romanized_name', 'name']
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

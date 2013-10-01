from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import Event, Performance, Venue


class PerformanceInline(admin.StackedInline):
    allow_add = True
    extra = 1
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'event', 'venue', 'day', ('start_time', 'end_time'))}),)
    model = Performance
    autocomplete_lookup_fields = {'fk': ['event', 'venue']}


class EventAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Dates', {'fields': ('start_date', 'end_date')}),
        ('Names', {'fields': (('romanized_name', 'name'), 'nickname', 'slug')}),
        ('Links', {'fields': ('info_link', 'secondary_info_link')}),
    )
    inlines = [PerformanceInline]
    list_display = ['romanized_name', 'name', 'nickname', 'start_date', 'end_date']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    save_on_top = True
    search_fields = ['romanized_name', 'name']
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'day'
    fieldsets = (
        (None, {'fields': ('event', 'venue')}),
        ('Dates', {'fields': ('day', ('start_time', 'end_time'))}),
        ('Names', {'fields': (('romanized_name', 'name'),)}),
    )
    list_display = ['romanized_name', 'name', 'day', 'start_time', 'end_time', 'event', 'venue']
    list_display_links = ['romanized_name', 'name']
    list_select_related = True
    save_on_top = True
    search_fields = ['day', 'start_time', 'end_time', 'event', 'venue']

    raw_id_fields = ('event', 'venue')
    autocomplete_lookup_fields = {'fk': ['event', 'venue']}
admin.site.register(Performance, PerformanceAdmin)


class VenueAdmin(ContributorMixin, admin.ModelAdmin):
    fieldsets = (
        ('Names', {'fields': (('romanized_name', 'name'), 'former_names', 'slug')}),
        ('Details', {'fields': ('romanized_address', 'address', 'country')}),
    )
    list_display = ['romanized_name', 'name', 'former_names', 'romanized_address', 'country']
    list_display_links = ['romanized_name', 'name']
    prepopulated_fields = {'slug': ['romanized_name']}
    save_on_top = True
    search_fields = ['romanized_name', 'name', 'country']
admin.site.register(Venue, VenueAdmin)

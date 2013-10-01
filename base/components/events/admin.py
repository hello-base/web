from django.contrib import admin

from .models import Event, Performance, Venue


class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)


class PerformanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Performance, PerformanceAdmin)


class VenueAdmin(admin.ModelAdmin):
    pass
admin.site.register(Venue, VenueAdmin)

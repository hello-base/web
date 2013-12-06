# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Correlation


class CorrelationAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Subject', {'fields': (('content_type', 'identifier'), 'object_id')}),
        ('Correlation Details', {'fields': ('timestamp', 'description')}),
        ('Derived Data', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('year', 'month', 'day'), 'julian')
        })
    )
    list_display = ['content_object', 'content_type', 'timestamp', 'date_field']
    list_filter = ['content_type', 'date_field']

    autocomplete_lookup_fields = {'generic': [['content_type', 'object_id']]}
    readonly_fields = ['identifier', 'year', 'month', 'day', 'julian']
admin.site.register(Correlation, CorrelationAdmin)

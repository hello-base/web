# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Fact, Summary


class FactInline(admin.StackedInline):
    extra = 1
    fields = ['body']
    model = Fact


class SummaryInline(admin.StackedInline):
    extra = 1
    fields = ['body', 'submitted_by']
    model = Summary

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'submitted_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(SummaryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

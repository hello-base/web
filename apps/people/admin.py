# -*- coding: utf-8 -*-
from django.contrib import admin

from base.apps.accounts.admin import ContributorMixin
from base.apps.prose.admin import FactInline

from .models import (Designation, Group, Groupshot, Headshot, Idol, Membership,
    Staff)


class DesignationInline(admin.TabularInline):
    extra = 1
    model = Designation


class GroupshotInline(admin.TabularInline):
    extra = 1
    model = Groupshot


class HeadshotInline(admin.TabularInline):
    extra = 1
    model = Headshot


class MembershipInline(admin.TabularInline):
    extra = 1
    model = Membership

    raw_id_fields = ['group']
    autocomplete_lookup_fields = {'fk': ['group']}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(MembershipInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'idol' or db_field.name == 'group':
            formfield.choices = formfield.choices
        return formfield


class GroupMembershipInline(MembershipInline):
    raw_id_fields = ['idol']
    autocomplete_lookup_fields = {'fk': ['idol']}


class IdolMembershipInline(MembershipInline):
    raw_id_fields = ['group']
    autocomplete_lookup_fields = {'fk': ['group']}


class GroupAdmin(ContributorMixin):
    date_hierarchy = 'started'
    fieldsets = (
        ('Status', {'fields': ('classification', ('status', 'scope'))}),
        ('Basics', {'fields': (('romanized_name', 'name'), 'slug')}),
        ('Dates', {'fields': (('started', 'ended'),)}),
        ('Parents & Children', {'fields': ('parent', 'groups')}),
        ('Details & Options', {'fields': ('former_names', ('photo', 'photo_thumbnail',))}),
        ('Internal Notes', {'fields': ('note',)}),
    )
    inlines = [
        DesignationInline,
        GroupMembershipInline,
        GroupshotInline,
        FactInline
    ]
    list_display = ['romanized_name', 'name', 'started', 'ended', 'classification', 'status', 'scope']
    list_editable = ['classification', 'status', 'scope']
    list_filter = ['classification', 'status', 'scope']
    prepopulated_fields = {'slug': ['romanized_name']}
    readonly_fields = ['photo', 'photo_thumbnail']
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('parent', 'groups',)
    autocomplete_lookup_fields = {
        'fk': ['parent'],
        'm2m': ['groups'],
    }
admin.site.register(Group, GroupAdmin)


class IdolAdmin(ContributorMixin):
    fieldsets = (
        ('Status', {'fields': (('status', 'scope'),)}),
        ('Basics', {'fields': (('romanized_name', 'name'), ('romanized_family_name', 'romanized_given_name'), ('family_name', 'given_name'), ('romanized_alias', 'alias'), 'nicknames', 'slug')}),
        ('Dates', {'fields': (('started', 'graduated', 'retired'),)}),
        ('Birth Details', {'fields': ('birthdate', ('birthplace_romanized', 'birthplace'), ('birthplace_latitude', 'birthplace_longitude'))}),
        ('Details & Options', {'fields': ('color', ('height', 'bloodtype'), ('photo', 'photo_thumbnail',))}),
        ('Internal Notes', {'fields': ('note',)}),
    )
    inlines = [IdolMembershipInline, HeadshotInline, FactInline]
    list_display = ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name', 'birthdate', 'status', 'scope', 'started', 'graduated', 'retired']
    list_display_links = ['romanized_family_name', 'romanized_given_name']
    list_editable = ['status', 'scope']
    list_filter = ['status', 'scope']
    prepopulated_fields = {'slug': ['romanized_family_name', 'romanized_given_name']}
    readonly_fields = ['romanized_name', 'name', 'photo', 'photo_thumbnail']
    search_fields = ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name', 'romanized_alias', 'alias']
admin.site.register(Idol, IdolAdmin)


class StaffAdmin(ContributorMixin):
    fieldsets = (
        (None, {'fields': (('romanized_family_name', 'romanized_given_name'), ('family_name', 'given_name'), ('romanized_alias', 'alias'), 'nicknames', 'slug')}),
    )
    list_display = ['romanized_family_name', 'romanized_given_name', 'romanized_alias', 'family_name', 'given_name', 'alias']
    list_display_links = ['romanized_family_name', 'romanized_given_name', 'romanized_alias']
    prepopulated_fields = {'slug': ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name']}
    search_fields = ['romanized_family_name', 'romanized_given_name']
admin.site.register(Staff, StaffAdmin)

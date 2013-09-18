from django.contrib import admin

from markdown import markdown
from typogrify.templatetags.typogrify_tags import typogrify

from .models import Group, Idol, Membership, Staff


class MembershipInline(admin.TabularInline):
    allow_add = True
    extra = 1
    model = Membership


class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'started'
    fieldsets = (
        ('Status', {'fields': ('classification', ('status', 'scope'))}),
        ('Basics', {'fields': (('romanized_name', 'name'), 'slug')}),
        ('Age', {'fields': (('started', 'ended'),)}),
        ('Parents & Children', {'fields': ('parent', 'groups')}),
        ('Details & Options', {'fields': ('former_names', 'note', 'has_discussions')}),
    )
    filter_horizontal = ['groups']
    inlines = [MembershipInline]
    list_display = ['romanized_name', 'name', 'started', 'ended', 'classification', 'status', 'scope']
    list_editable = ['classification', 'status', 'scope']
    prepopulated_fields = {'slug': ['romanized_name']}
    save_on_top = True
    search_fields = ['romanized_name', 'name']

    raw_id_fields = ('parent', 'groups',)
    autocomplete_lookup_fields = {
        'fk': ['parent'],
        'm2m': ['groups'],
    }

    def save_model(self, request, obj, form, change):
        obj.note_processed = typogrify(markdown(obj.note, ('footnotes',)))
        obj.save()
admin.site.register(Group, GroupAdmin)


class IdolAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {'fields': (('status', 'scope'),)}),
        ('Basics', {'fields': (('romanized_family_name', 'romanized_given_name'), ('family_name', 'given_name'), ('romanized_alias', 'alias'), 'nicknames', 'slug')}),
        ('Birth Details', {'fields': ('birthdate', ('birthplace_romanized', 'birthplace'), ('birthplace_latitude', 'birthplace_longitude'))}),
        ('Details & Options', {'fields': ('height', 'bloodtype', 'note', 'has_discussions')}),
    )
    inlines = [MembershipInline]
    list_display = ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name', 'birthdate', 'status', 'scope']
    list_editable = ['status', 'scope']
    prepopulated_fields = {'slug': ['romanized_family_name', 'romanized_given_name']}
    save_on_top = True
    search_fields = ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name', 'romanized_alias', 'alias']

    def save_model(self, request, obj, form, change):
        obj.note_processed = typogrify(markdown(obj.note, ('footnotes',)))
        obj.save()
admin.site.register(Idol, IdolAdmin)


class StaffAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('romanized_family_name', 'romanized_given_name'), ('family_name', 'given_name'), ('romanized_alias', 'alias'), 'nicknames', 'slug')}),
    )
    list_display = ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name', 'romanized_alias', 'alias']
    prepopulated_fields = {'slug': ['romanized_family_name', 'romanized_given_name', 'family_name', 'given_name']}
    save_on_top = True
    search_fields = ['romanized_family_name', 'romanized_given_name']
admin.site.register(Staff, StaffAdmin)
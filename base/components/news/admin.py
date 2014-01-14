# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Item, ItemImage, SUBJECTS, Update

subject_fields = ['%ss' % subject._meta.model_name for subject in SUBJECTS]


class ItemImageInline(admin.TabularInline):
    extra = 1
    model = ItemImage


class UpdateInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': (('author', 'published'), 'body', ('source', 'source_url'), ('via', 'via_url'))}),)
    model = Update

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(UpdateInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    fieldsets = (
        (None, {'fields': ('author',)}),
        ('Basics', {'fields': ('title', 'slug', ('published', 'category', 'classification'))}),
        ('Body', {'fields': ('body',)}),
        ('Correlations', {
            'description': 'Selecting a correlation will display this news item wherever happenings are displayed.',
            'fields': ('correlations',)
        }),
        ('Involvement', {
            'description': 'Only add idols if news specifically relates to them, i.e. not if the news is about their group.',
            'fields': tuple(subject_fields)
        }),
        ('Sources', {'fields': (('source', 'source_url'), ('via', 'via_url'))}),
    )
    inlines = [ItemImageInline, UpdateInline]
    list_display = ['title', 'published', 'category', 'author', 'via']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'author']

    raw_id_fields = ['correlations'] + subject_fields
    autocomplete_lookup_fields = {'m2m': ['correlations'] + subject_fields}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Item, ItemAdmin)

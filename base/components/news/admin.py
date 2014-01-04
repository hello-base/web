from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import Item, Update


class UpdateInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': ('date', 'author', 'body', ('source', 'source_url'), ('via', 'via_url'))}),)
    model = Update


class ItemAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        ('Basics', {'fields': ('category', 'title', 'date', 'author')}),
        ('Body', {'fields': ('body',)}),
        ('Involvement', {
            'description': 'Only add idols if news specifically relates to them, i.e. not if the news is about their group.',
            'fields': ('idols', 'groups', 'singles', 'albums', 'events')}),
        ('Sources', {'fields': (('source', 'source_url'), ('via', 'via_url'))}),
    )
    inlines = [UpdateInline]
    list_display = ['title', 'date', 'category', 'author', 'via']
    search_fields = ['title', 'author']

    raw_id_fields = ('idols', 'groups', 'singles', 'albums', 'events')
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups', 'singles', 'albums', 'events']}
admin.site.register(Item, ItemAdmin)
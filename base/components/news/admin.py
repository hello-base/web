from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import Item, ItemImage, Update


class ItemImageInline(admin.TabularInline):
    extra = 1
    model = ItemImage


class UpdateInline(admin.StackedInline):
    extra = 1
    fieldsets = ((None, {'fields': ('author', 'published', 'body', ('source', 'source_url'), ('via', 'via_url'))}),)
    model = Update


class ItemAdmin(ContributorMixin, admin.ModelAdmin):
    date_hierarchy = 'published'
    fieldsets = (
        (None, {'fields': ('author',)}),
        ('Basics', {'fields': ('title', ('category', 'published', 'slug'))}),
        ('Body', {'fields': ('body',)}),
        ('Involvement', {
            'description': 'Only add idols if news specifically relates to them, i.e. not if the news is about their group.',
            'fields': ('idols', 'groups', 'singles', 'albums', 'events')}),
        ('Sources', {'fields': (('source', 'source_url'), ('via', 'via_url'))}),
    )
    inlines = [ItemImageInline, UpdateInline]
    list_display = ['title', 'published', 'category', 'author', 'via']
    search_fields = ['title', 'author']

    raw_id_fields = ('idols', 'groups', 'singles', 'albums', 'events')
    autocomplete_lookup_fields = {'m2m': ['idols', 'groups', 'singles', 'albums', 'events']}
admin.site.register(Item, ItemAdmin)

from django.contrib import admin

from components.accounts.admin import ContributorMixin

from .models import Item, Update

class ItemAdmin(ContributorMixin, admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': ('category', 'title', 'date', 'author')}),
        ('Body', {'fields': ('body',)}),
        ('Involvement', {'fields': ('idols', 'groups', 'singles', 'albums', 'events')}),
        ('Sources', {'fields': (('source', 'source_url'), ('via', 'via_url'))}),
    )
admin.site.register(Item, ItemAdmin)
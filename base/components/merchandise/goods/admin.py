from django.contrib import admin

from .models import Good, Set, Shop, SuperSet


class GoodAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('romanized_name', 'name'), ('price', 'link'), ('available_from', 'available_until'), 'image')}),
        ('Sources', {'fields': ('event', 'shop', 'online_id', 'other_info')}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        })
        # (None, {'fields': ('',)})
    )
    readonly_fields = ['participating_idols', 'participating_groups']

    raw_id_fields = ('event', 'idols', 'groups', 'shop',)
    autocomplete_lookup_fields = {
        'fk': ['event', 'shop'],
        'm2m': ['idols', 'groups']
    }
admin.site.register(Good, GoodAdmin)


class SetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Set, SetAdmin)


class ShopAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shop, ShopAdmin)


class SuperSetAdmin(admin.ModelAdmin):
    pass
admin.site.register(SuperSet, SuperSetAdmin)

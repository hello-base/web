from django.contrib import admin

from .models import Good, Set, Shop, SuperSet


class BaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('romanized_name', 'name'),)}),
        ('Details', {'fields': (('price', 'link'), ('available_from', 'available_until'), 'image')}),
        ('Sources', {'fields': ('event', 'shop', 'online_id', 'other_info')}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Options', {'fields': (('is_graduation_good', 'is_birthday_good'), ('is_online_exclusive', 'is_mailorder_exclusive'))})
    )
    list_display = ['romanized_name', 'name', 'price', 'available_from', 'available_until', 'event', 'shop', 'online_id']
    readonly_fields = ['participating_idols', 'participating_groups']

    raw_id_fields = ('event', 'idols', 'groups', 'shop',)
    autocomplete_lookup_fields = {
        'fk': ['event', 'shop'],
        'm2m': ['idols', 'groups']
    }


class GoodAdmin(BaseAdmin):
    def get_fieldsets(self, request, obj=None):
        fs = super(GoodAdmin, self).get_fieldsets(request, obj)
        # fs now contains [(None, {'fields': fields})], do with it whatever you want
        # all_fields = fs[0][1]['fields']
        return fs
admin.site.register(Good, GoodAdmin)


class SetAdmin(BaseAdmin):
    pass
admin.site.register(Set, SetAdmin)


class ShopAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'slug', 'website_link',)}),)
    list_display = ['romanized_name', 'name', 'website_link']
admin.site.register(Shop, ShopAdmin)


class SuperSetAdmin(BaseAdmin):
    pass
admin.site.register(SuperSet, SuperSetAdmin)

from django.contrib import admin

from .models import Good, Set, Shop, SuperSet


class BaseAdmin(admin.ModelAdmin):
    list_display = ['romanized_name', 'name', 'price', 'available_from', 'available_until', 'event', 'shop', 'online_id']
    readonly_fields = ['participating_idols', 'participating_groups']

    raw_id_fields = ('event', 'idols', 'groups', 'shop',)
    autocomplete_lookup_fields = {
        'fk': ['event', 'shop'],
        'm2m': ['idols', 'groups']
    }


class GoodAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'category')}),
        (None, {'fields': (('romanized_name', 'name'),)}),
        ('Details', {'fields': (('available_from', 'available_until'), ('price', 'link'), 'image')}),
        ('Sources', {'fields': ('event', 'shop', 'online_id', 'other_info')}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Options', {'fields': (
            ('is_bonus_good', 'is_campaign_good'),
            ('is_lottery_good', 'is_set_exclusive'),
            ('is_graduation_good', 'is_birthday_good'),
            ('is_online_exclusive', 'is_mailorder_exclusive'),
        )})
    )

    raw_id_fields = ('event', 'idols', 'groups', 'shop', 'parent',)
    autocomplete_lookup_fields = {
        'fk': ['parent', 'event', 'shop'],
        'm2m': ['idols', 'groups']
    }
admin.site.register(Good, GoodAdmin)


class SetAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('category',)}),
        (None, {'fields': (('romanized_name', 'name'),)}),
        ('Details', {'fields': (('available_from', 'available_until'), ('price', 'link'), 'image')}),
        ('Sources', {'fields': ('event', 'shop', 'online_id', 'other_info')}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Options', {'fields': (
            ('is_graduation_good', 'is_birthday_good'),
            ('is_online_exclusive', 'is_mailorder_exclusive'),
        )})
    )
admin.site.register(Set, SetAdmin)


class ShopAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('romanized_name', 'name'), 'slug', 'website_link',)}),)
    list_display = ['romanized_name', 'name', 'website_link']
admin.site.register(Shop, ShopAdmin)


class SuperSetAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('goods', 'sets',)}),
        (None, {'fields': (('romanized_name', 'name'),)}),
        ('Details', {'fields': (('available_from', 'available_until'), ('price', 'link'), 'image')}),
        ('Sources', {'fields': ('event', 'shop', 'online_id', 'other_info')}),
        ('Participants', {'fields': ('idols', 'groups')}),
        ('Participants (Rendered)', {
            'classes': ('grp-collapse grp-closed',),
            'description': 'This is calculated by the values inputted in "Participants."',
            'fields': ('participating_idols', 'participating_groups')
        }),
        ('Options', {'fields': (
            ('is_graduation_good', 'is_birthday_good'),
            ('is_online_exclusive', 'is_mailorder_exclusive'),
        )})
    )

    raw_id_fields = ('goods', 'sets', 'event', 'idols', 'groups', 'shop',)
    autocomplete_lookup_fields = {
        'fk': ['event', 'shop'],
        'm2m': ['goods', 'sets', 'idols', 'groups']
    }
admin.site.register(SuperSet, SuperSetAdmin)

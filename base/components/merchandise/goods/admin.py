from django.contrib import admin

from .models import Good, Set, Shop, SuperSet


class GoodAdmin(admin.ModelAdmin):
    pass
admin.register(Good, GoodAdmin)


class SetAdmin(admin.ModelAdmin):
    pass
admin.register(Set, SetAdmin)


class ShopAdmin(admin.ModelAdmin):
    pass
admin.register(Shop, ShopAdmin)


class SuperSetAdmin(admin.ModelAdmin):
    pass
admin.register(SuperSet, SuperSetAdmin)

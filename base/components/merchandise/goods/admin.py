from django.contrib import admin

from .models import Good, Set, Shop, SuperSet


class GoodAdmin(admin.ModelAdmin):
    pass
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

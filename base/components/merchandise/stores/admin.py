# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import PurchaseLink, Store


class PurchaseLinkInline(admin.TabularInline):
    extra = 1
    fields = ['store', 'url']
    model = PurchaseLink


class PurchaseLinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(PurchaseLink, PurchaseLinkAdmin)


class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)

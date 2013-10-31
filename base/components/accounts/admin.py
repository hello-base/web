from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Editor


class ContributorMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.submitted_by = request.user
        obj.edited_by.add(request.user)
        obj.save()
        super(ContributorMixin, self).save_model(request, obj, form, change)


class EditorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('username', 'password'),)}),
        ('Personal Information', {'fields': (('name', 'email'),)}),
        ('Important Dates', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('started', 'last_login', 'active_since')
        }),
        ('Permissions', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('is_active', 'is_staff', 'is_superuser'),)
        }),
        ('OAuth', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('base_id', ('access_token', 'refresh_token', 'token_expiration'))
        })
    )
    list_display = ['username', 'name', 'email', 'is_active', 'is_staff', 'is_superuser', 'base_id', 'access_token']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
admin.site.register(Editor, EditorAdmin)
admin.site.unregister(Group)

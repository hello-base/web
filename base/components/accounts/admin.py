from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Editor


class ContributorMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super(ContributorMixin, self).save_model(request, obj, form, change)
        if not change:
            obj.submitted_by = request.user
        obj.edited_by.add(request.user)
        obj.save()


class EditorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('name', 'email')}),
        ('Important Dates', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('started', 'last_login', 'active_since')
        }),
        ('Permissions', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_active', 'is_staff', 'is_superuser')
        })
    )
    list_display = ['username', 'name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
admin.site.register(Editor, EditorAdmin)
admin.site.unregister(Group)

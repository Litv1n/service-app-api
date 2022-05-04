from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Restaurant, Menu


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', )}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Importand dates'), {'fields': ('last_login', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Restaurant)
admin.site.register(Menu)

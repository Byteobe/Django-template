from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'status', 'status_delivery', 'groups_name')
    search_fields = ('id', 'username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Status'), {'fields': ('status', 'status_delivery')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    def groups_name(self, obj):
        if obj.groups.exists():
            return ", ".join(group.name for group in obj.groups.all())
        return _("No roles")

    groups_name.short_description = _("Roles")


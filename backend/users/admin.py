from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {'fields': (
                'email', 'username', 'first_name',
                'last_name', 'password1', 'password2', 'is_distributor',
                'is_supplier', 'is_dealer'
            )
            }
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Fields', {
                'fields': ('is_distributor', 'is_supplier', 'is_dealer')
                }
            ),
    )
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
        'is_distributor',
        'is_supplier',
        'is_dealer'
    )
    list_filter = ('email', 'username')
    search_fields = ('email', 'username',)
    empty_value_display = '-empty-'

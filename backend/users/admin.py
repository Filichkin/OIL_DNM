from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Dealer, Supplier, User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {'fields': (
                'email', 'username', 'first_name', 'rs_code', 'supplier',
                'last_name', 'password1', 'password2', 'is_distributor',
                'is_supplier', 'is_dealer', 'is_dealer_admin'
            )
            }
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Fields', {
                'fields': (
                    'is_distributor',
                    'is_supplier',
                    'is_dealer',
                    'is_dealer_admin',
                    'rs_code',
                    'supplier',
                    'phone',
                    )
                }
            ),
    )
    list_display = (
        'username',
        'id',
        'email',
        'phone',
        'first_name',
        'last_name',
        'is_distributor',
        'is_supplier',
        'is_dealer',
        'is_dealer_admin'
    )
    list_filter = ('email', 'username')
    search_fields = ('email', 'username',)
    empty_value_display = '-empty-'


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = (
        'rs_code',
        'name',
        'inn',
        'legal_address',
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'legal_name',
        'inn',
        'phone',
        'contact_name',
        'contact_job_title',
        'address',
        'legal_address'
    )

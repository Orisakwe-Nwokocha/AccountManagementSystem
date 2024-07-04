from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'first_name', 'last_name', 'email', 'phone'),
            },
        ),
    )
    # list_display = ['first_name', 'last_name', 'username', 'email', 'phone']
    # list_per_page = 10
    # search_fields = ['account_number', 'account_type']
    # list_editable = ['account_type',]
    # list_filter = ['account_number', 'account_type']

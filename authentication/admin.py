from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.user_model import User

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ("email", "date_joined", "last_login", "is_superuser", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")
    ordering = ["email"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    filter_horizontal = ()
    list_filter = ()    
    fieldsets = ()


admin.site.register(User, AccountAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
        "__str__",
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")
    ordering = ["first_name"]

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

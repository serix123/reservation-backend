from django.contrib import admin
from reservation.models import Department

from reservation.models import Employee

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

    list_display = (
        "__str__",
        "immediate_head",
        "department",
        "is_admin",
        "date_joined",
    )
    ordering = ["first_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "immediate_head",
                    "department",
                    "show_is_admin",
                ),
            },
        ),
    )

    def is_admin(self, obj):
        return obj.is_admin

    is_admin.short_description = "Admin Status"
    is_admin.boolean = True

    def date_joined(self, obj):
        return obj.date_joined

    date_joined.short_description = "Date Joined"


class DepartmentAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "name",
        "superior",
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)

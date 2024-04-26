from django.contrib import admin

from reservation.models.employee_model import Employee

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "immediate_head",
                    "department",
                    "employee_type"
                ),
            },
        ),
    )


admin.site.register(Employee, EmployeeAdmin)

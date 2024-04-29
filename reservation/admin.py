from django.contrib import admin
from recurrence.forms import RecurrenceField
from reservation.models import Department, Employee, Equipment, Event, Facility

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

    list_display = (
        "id",
        "__str__",
        "immediate_head",
        "department",
        "is_admin",
        "date_joined",
    )
    ordering = ["id"]
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


class FacilityAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "id",
        "name",
        "department",
        "person_in_charge",
    )


class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "equipment_name",
        "equipment_type",
        "equipment_quantity",
        "work_type",
    ]
    list_filter = ["equipment_type"]
    search_fields = ["equipment_name", "equipment_type"]
    ordering = ["equipment_name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "organizer_name", "start_time", "end_time", "status"]
    list_filter = [
        "event_name",
        "organizer_name",
        "status",
        "reserved_facility",
        "department",
        "start_time",
    ]
    search_fields = ["organizer_name", "department"]
    formfield_overrides = {
        RecurrenceField: {"widget": RecurrenceField.widget},
    }


admin.site.register(Event, EventAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)

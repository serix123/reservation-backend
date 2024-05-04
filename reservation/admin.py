from django.contrib import admin
# from recurrence.forms import RecurrenceField
from reservation.models import (
    Department,
    Employee,
    Equipment,
    Event,
    EventEquipment,
    Facility,
    Approval,
)

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
        "immediate_head",
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


class EventEquipmentInline(admin.TabularInline):
    model = EventEquipment
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "event_name", "requesitioner_name",
                    "start_time", "end_time", "status"]
    list_filter = [
        "event_name",
        "requesitioner",
        "status",
        "reserved_facility",
        "department",
        "start_time",
    ]
    search_fields = ["event_name", "requesitioner", "department"]

    inlines = (EventEquipmentInline,)

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'application':
            super().save_model(request, obj, form, change)
            if not hasattr(obj, 'approval'):
                Approval.objects.create(
                    event=obj, requesitioner=obj.requesitioner)
        else:
            super().save_model(request, obj, form, change)
    # formfield_overrides = {
    #     RecurrenceField: {"widget": RecurrenceField.widget},
    # }


class ApprovalAdmin(admin.ModelAdmin):
    readonly_fields = ("id",
                       'immediate_head_approver',
                       'person_in_charge_approver',)
    list_display = ["__str__", 'event', 'requesitioner', 'immediate_head_approver', 'person_in_charge_approver',
                    'status', 'get_immediate_head_status', 'get_person_in_charge_status']
    actions = ['make_approved']

    def get_immediate_head_status(self, obj):
        return obj.immediate_head_approval
    get_immediate_head_status.short_description = 'Immediate Head Status'

    def get_person_in_charge_status(self, obj):
        return obj.person_in_charge_approval
    get_person_in_charge_status.short_description = 'Person in Charge Status'

    def get_admin_status(self, obj):
        return obj.admin_approval
    get_admin_status.short_description = 'Admin Status'

    def make_approved(self, request, queryset):
        for approval in queryset:
            approval.immediate_head_approved = 1
            approval.person_in_charge_approved = 1
            approval.admin_approved = 1
            approval.check_if_approved()
            approval.save()
    make_approved.short_description = "Mark selected as approved"


admin.site.register(Approval, ApprovalAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)

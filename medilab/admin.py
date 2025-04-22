from django.contrib import admin
from medilab.models import Patient


# @admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user_email",
        "dob",
        "verification_status",
        "created_at",
    )
    list_filter = ("verification_status", "gender", "created_at")
    search_fields = ("first_name", "last_name", "user__email")
    readonly_fields = ("created_at", "updated_at")
    actions = ["verify_patients", "reject_patients"]

    fieldsets = (
        (None, {"fields": ("user", "verification_status")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "dob", "gender")}),
        ("Contact Info", {"fields": ("contact_number", "address")}),
        ("Documents", {"fields": ("id_document",)}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"
    user_email.admin_order_field = "user__email"

    @admin.action(description="Mark selected patients as verified")
    def verify_patients(self, request, queryset):
        updated = queryset.update(verification_status="verified")
        self.message_user(request, f"{updated} patients verified successfully")

    @admin.action(description="Mark selected patients as rejected")
    def reject_patients(self, request, queryset):
        updated = queryset.update(verification_status="rejected")
        self.message_user(request, f"{updated} patients rejected")


admin.site.register(Patient, PatientAdmin)

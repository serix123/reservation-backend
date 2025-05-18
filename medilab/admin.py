from django.contrib import admin
from medilab.models import PatientProfile, PatientProfileApplication
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


# class PatientProfileApplicationAdmin(admin.ModelAdmin):
#     list_display = (
#         "user_full_name",
#         "application_type",
#         "village",
#         "status",
#         "created_at",
#         "review_status",
#         "application_actions",
#     )
#     list_filter = ("status", "village", "created_at")
#     search_fields = ("user__first_name", "user__last_name", "village", "address")
#     readonly_fields = (
#         "created_at",
#         "updated_at",
#         "review_date",
#         "reviewed_by",
#         "id_proof_preview",
#     )
#     fieldsets = (
#         (None, {"fields": ("user", "status", "reviewed_by", "review_date")}),
#         (
#             "Patient Information",
#             {"fields": ("date_of_birth", "address", "village", "medical_history")},
#         ),
#         (
#             "ID Proof",
#             {"fields": ("id_proof_filename", "id_proof_base64", "id_proof_preview")},
#         ),
#         (
#             "Timestamps",
#             {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
#         ),
#     )

#     # NEW HELPER METHOD:
#     def application_type(self, obj):
#         """Displays whether application is new or update"""
#         return "Update" if obj.is_update else "New"

#     application_type.short_description = "Type"

#     def user_full_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"

#     user_full_name.short_description = "User"

#     def review_status(self, obj):
#         if obj.status == "approved":
#             color = "green"
#         elif obj.status == "rejected":
#             color = "red"
#         else:
#             color = "orange"
#         return format_html(
#             '<span style="color: {};">{}</span>', color, obj.get_status_display()
#         )

#     review_status.short_description = "Status"

#     def id_proof_preview(self, obj):
#         if obj.id_proof_base64:
#             return mark_safe(
#                 f'<img src="data:image/jpeg;base64,{obj.id_proof_base64}" '
#                 f'style="max-width: 300px; max-height: 300px;" />'
#             )
#         return "No ID proof uploaded"

#     id_proof_preview.short_description = "ID Proof Preview"

#     def application_actions(self, obj):  # Renamed from 'actions' to avoid conflict
#         if obj.status == "pending":
#             approve_url = reverse(
#                 "admin:medilab_patientprofileapplication_approve", args=[obj.id]
#             )
#             reject_url = reverse(
#                 "admin:medilab_patientprofileapplication_reject", args=[obj.id]
#             )
#             return format_html(
#                 '<a class="button" href="{}">Approve</a>&nbsp;'
#                 '<a class="button" href="{}">Reject</a>',
#                 approve_url,
#                 reject_url,
#             )
#         return ""

#     application_actions.short_description = "Actions"
#     application_actions.allow_tags = True

#     def get_urls(self):
#         from django.urls import path

#         urls = super().get_urls()
#         custom_urls = [
#             path(
#                 "<int:pk>/approve/",
#                 self.admin_site.admin_view(self.approve_application),
#                 name="medilab_patientprofileapplication_approve",
#             ),
#             path(
#                 "<int:pk>/reject/",
#                 self.admin_site.admin_view(self.reject_application),
#                 name="medilab_patientprofileapplication_reject",
#             ),
#         ]
#         return custom_urls + urls

#     def approve_application(self, request, pk):
#         try:
#             application = PatientProfileApplication.objects.get(pk=pk)
#             if application.approve(request.user):
#                 self.message_user(
#                     request, "Application approved and archived successfully"
#                 )
#             else:
#                 self.message_user(request, "Approval failed", level="ERROR")
#         except PatientProfileApplication.DoesNotExist:
#             self.message_user(request, "Application not found", level="ERROR")

#         # Redirect back to the applications list
#         return self.response_post_save_change(request, None)

#     def reject_application(self, request, pk):
#         application = PatientProfileApplication.objects.get(pk=pk)
#         application.reject(request.user)
#         self.message_user(request, "Application rejected")
#         return self.response_post_save_change(request, application)


# class PatientProfileAdmin(admin.ModelAdmin):
#     list_display = ("user_full_name", "village", "approval_date", "approved_by")
#     list_filter = ("village", "approval_date")
#     search_fields = ("user__first_name", "user__last_name", "village", "address")
#     readonly_fields = ("created_at", "updated_at", "approval_date")
#     fieldsets = (
#         (None, {"fields": ("user", "approved_by", "approval_date")}),
#         (
#             "Patient Information",
#             {"fields": ("date_of_birth", "address", "village", "medical_history")},
#         ),
#         (
#             "Timestamps",
#             {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
#         ),
#     )

#     def user_full_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"

#     user_full_name.short_description = "User"


# admin.site.register(PatientProfile, PatientProfileAdmin)
# admin.site.register(PatientProfileApplication, PatientProfileApplicationAdmin)

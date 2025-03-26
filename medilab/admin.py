from django.contrib import admin
from medilab.models import Patient, MedicalRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Customized admin interface for Patient model.
    Provides enhanced list display and filtering capabilities.
    """
    list_display = (
        'id',
        'full_name',
        'user',
        'gender',
        'birthdate'
    )

    list_filter = (
        'gender',
        'birthdate'
    )

    search_fields = (
        'first_name',
        'last_name',
        'user__username'
    )

    readonly_fields = ('id',)  # Prevent ID modification

    def full_name(self, obj):
        """
        Custom method to display full name in admin list view.
        """
        return obj.get_full_name()
    full_name.short_description = 'Full Name'


@admin.register(MedicalRecord)
class RecordAdmin(admin.ModelAdmin):
    """
    Customized admin interface for Patient model.
    Provides enhanced list display and filtering capabilities.
    """
    list_display = (
        'id',
        'patient',
        'visit_date',
        'diagnosis_category',
        'diagnosis_details',
        'treatment'
    )

    list_filter = (
        'attending_doctor',
        'patient'
    )

    search_fields = (
        'patient',
        'attending_doctor',
    )

    readonly_fields = ('id', 'patient',)  # Prevent ID modification

    def summary(self, obj):
        """
        Custom method to display full name in admin list view.
        """
        return obj.get_summary()
    summary.short_description = 'Record summary'

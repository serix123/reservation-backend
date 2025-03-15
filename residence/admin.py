from django.contrib import admin
from django.utils import timezone
from residence.models import (Residence, Visitor, Event, Issue)


class ResidenceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "role",
        "contact_number",
        "address",
        "registration_date",
    ]
    list_filter = ["role"]
    search_fields = ["first_name", "last_name", "role"]
    ordering = ["first_name", "last_name", "role"]


class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        'name',
        'status',
        'residence',
        'visit_date',
        'visit_purpose',
    ]
    list_filter = ["status"]
    search_fields = ["name", "visit_date", "residence"]
    ordering = ["name", "visit_date", "residence"]


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'resident',
                    'reported_date', 'resolved_date')
    list_filter = ('status', 'reported_date', 'resolved_date')
    search_fields = ('title', 'description', 'resident__user__email')
    raw_id_fields = ('resident',)
    date_hierarchy = 'reported_date'
    readonly_fields = ('reported_date', 'resolved_date')

    fieldsets = (
        ('Issue Details', {
            'fields': ('title', 'description', 'status')
        }),
        ('Resident Info', {
            'fields': ('resident',)
        }),
        ('Timestamps', {
            'fields': ('reported_date', 'resolved_date')
        }),
    )

    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(
            status=Issue.IssueStatus.RESOLVED,
            resolved_date=timezone.now()
        )
    mark_as_resolved.short_description = "Mark selected issues as resolved"


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'creator',
                    'attendees_count', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('name', 'location', 'details', 'creator__email')
    filter_horizontal = ('attendees',)
    raw_id_fields = ('creator',)
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at', 'attendees_count')

    fieldsets = (
        ('Event Details', {
            'fields': ('name', 'date', 'details', 'location')
        }),
        ('Organizer Info', {
            'fields': ('creator', 'attendees')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def attendees_count(self, obj):
        return obj.attendees.count()
    attendees_count.short_description = "Attendees"

    actions = ['send_event_reminders']

    def send_event_reminders(self, request, queryset):
        # Add your reminder logic here
        self.message_user(
            request, f"Reminders sent for {queryset.count()} events")
    send_event_reminders.short_description = "Send reminders for selected events"


admin.site.register(Residence, ResidenceAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Event, EventAdmin)

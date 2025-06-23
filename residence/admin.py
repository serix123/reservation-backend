from django.contrib import admin
from django.utils import timezone
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from residence.models import (
    CommunityDocument,
    CommunityResource,
    DocumentCategory,
    Event,
    Issue,
    IssueComment,
    Notice,
    Residence,
    Visitor,
)


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
        "name",
        "status",
        "residence",
        "visit_date",
        "visit_purpose",
    ]
    list_filter = ["status"]
    search_fields = ["name", "visit_date", "residence"]
    ordering = ["name", "visit_date", "residence"]


class IssueCommentInline(admin.TabularInline):  # or admin.StackedInline
    model = IssueComment
    extra = 1  # Number of empty forms shown
    fields = ["user", "comment", "created_at"]
    readonly_fields = ["created_at"]


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "user",
        "assigned_to",
        "reported_date",
        "resolved_date",
        "image_thumbnail",  # Added image_thumbnail
    )
    list_filter = (
        "status",
        "priority",  # Added priority to list filters
        "reported_date",
        "resolved_date",
    )
    search_fields = (
        "title",
        "description",
        "user__email",  # Changed 'resident__user__email' to 'user__email'
        "user__username",  # Added search by username
        "assigned_to__email",  # Changed 'resident__user__email' to 'user__email'
        "assigned_to__username",  # Added search by username
    )
    raw_id_fields = ("user", "assigned_to")  # Changed 'resident' to 'user'
    date_hierarchy = "reported_date"
    readonly_fields = ("reported_date", "resolved_date")
    inlines = [IssueCommentInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Status & Priority",
            {
                "fields": (
                    "status",
                    "priority",
                    "resolved_date",
                )
            },
        ),
        ("Reporter Information", {"fields": ("user", "assigned_to")}),
        ("Timestamps", {"fields": ("reported_date",)}),
    )

    actions = ["mark_as_resolved"]

    def mark_as_resolved(self, request, queryset):
        queryset.update(status=Issue.IssueStatus.RESOLVED, resolved_date=timezone.now())
        self.message_user(
            request,
            f"Marked {queryset.count()} issues as resolved.",
            level=admin.messages.SUCCESS,
        )

    mark_as_resolved.short_description = "Mark selected issues as resolved"

    def image_thumbnail(self, obj):
        if obj.image:
            from django.utils.html import format_html

            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image.url
            )
        return "No Image"

    image_thumbnail.short_description = "Image Preview"
    image_thumbnail.allow_tags = True


class EventAdmin(admin.ModelAdmin):
    # Fields displayed in the list view
    list_display = (
        "id",
        "name",
        "date",
        # "status",  # <<< Added: Display event status in the list
        "location",
        "creator",
        "attendees_count",
        "created_at",
        "image_thumbnail",
    )

    # Filters available in the right sidebar of the list view
    list_filter = (
        # "status",  # <<< Added: Allow filtering by event status
        "date",
        "created_at",
    )

    # Fields that can be searched using the search bar
    search_fields = (
        "name",
        "location",
        "details",
        "creator__username",
        "creator__email",
    )  # Adjusted creator search

    # Use a neat horizontal filter for ManyToMany fields
    filter_horizontal = ("attendees",)

    # Use a raw ID input for ForeignKey fields to prevent large dropdowns
    raw_id_fields = ("creator",)

    # Adds a date-based drilldown navigation for the 'date' field
    date_hierarchy = "date"

    # Fields that cannot be edited via the admin form
    # created_at and updated_at are handled by auto_now/auto_now_add
    # attendees_count is a @property and should not be editable
    readonly_fields = ("created_at", "updated_at", "attendees_count")

    # Organize fields into collapsible sections on the edit/add form
    fieldsets = (
        (
            "Event Details",
            {
                "fields": (
                    "name",
                    "date",
                    "image",
                    # "status",
                    "details",
                    "location",
                )  # <<< Added: status to event details
            },
        ),
        (
            "Organizer & Attendees",
            {"fields": ("creator", "attendees")},  # Renamed for clarity
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    # Custom method for displaying attendees count in list_display
    def attendees_count(self, obj):
        return obj.attendees.count()

    attendees_count.short_description = "Attendees"  # Label for the column

    # Custom actions available from the admin list view dropdown
    actions = ["send_event_reminders"]

    def send_event_reminders(self, request, queryset):
        # Your reminder logic would go here. Example:
        # from django.core.mail import send_mail
        # for event in queryset:
        #     # Iterate through event.attendees.all() and send emails
        #     pass
        self.message_user(
            request,
            f"Reminders initiated for {queryset.count()} events.",
            level=admin.messages.SUCCESS,  # Use Django messages for better feedback
        )

    send_event_reminders.short_description = "Send reminders for selected events"

    def image_thumbnail(self, obj):
        if obj.image:
            from django.utils.html import format_html

            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image.url
            )
        return "No Image"

    image_thumbnail.short_description = "Image Preview"
    image_thumbnail.allow_tags = True


class IssueCommentAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "comment_preview",  # A custom method to show a snippet of the comment
        "issue",
        "user",
        "created_at",
    )

    # Fields to use for filtering in the right sidebar
    list_filter = (
        "issue",
        "user",
        "created_at",
    )

    # Fields that can be searched using the search bar
    search_fields = (
        "comment",
        "issue__title",  # Allows searching comments by related issue's title
        "user__username",  # Allows searching comments by the user's username
        "user__email",  # Allows searching comments by the user's email
    )

    # Use a raw ID input for ForeignKey fields to avoid large dropdowns,
    # especially useful if you have many issues or users.
    raw_id_fields = (
        "issue",
        "user",
    )

    # Fields that cannot be edited via the admin form; auto-generated timestamps.
    readonly_fields = ("created_at",)

    # Organize fields into sections on the add/edit form
    fieldsets = (
        (
            None,
            {  # General details
                "fields": (
                    "issue",
                    "user",
                    "comment",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    # Custom method to display a short preview of the comment in the list view
    def comment_preview(self, obj):
        max_length = 75
        if len(obj.comment) > max_length:
            return f"{obj.comment[:max_length]}..."
        return obj.comment

    comment_preview.short_description = "Comment"  # Column header for this method

    # Optional: Date hierarchy for easy navigation by creation date
    date_hierarchy = "created_at"


class CommunityResourceAdmin(admin.ModelAdmin):
    list_display = ["name", "resource_type", "status", "managed_by"]
    search_fields = ["name", "managed_by__email"]
    list_filter = ["resource_type", "status"]
    readonly_fields = ["created_at", "updated_at"]


class DocumentCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the DocumentCategory model,
    supporting hierarchical display and management.
    """

    list_display = (
        "category_name",
        "parent",
        "get_full_path",  # Custom method to display full category path
        "get_subcategories_count",  # Custom method to display subcategory count
    )

    # Allows filtering categories by their parent
    list_filter = ("parent",)

    # Enables searching by category name
    search_fields = ("category_name",)

    # Use raw ID input for the parent ForeignKey to avoid large dropdowns
    raw_id_fields = ("parent",)

    # Organize fields on the add/edit form
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category_name",
                    "parent",
                )
            },
        ),
    )

    def get_subcategories_count(self, obj):
        """Returns the number of direct subcategories for the current category."""
        return obj.subcategories.count()

    get_subcategories_count.short_description = "Subcategories"  # Column header

    def get_full_path(self, obj):
        """Constructs and returns the full hierarchical path of the category."""
        path = [obj.category_name]
        current = obj
        while current.parent:
            current = current.parent
            path.insert(0, current.category_name)
        return " > ".join(path)

    get_full_path.short_description = "Full Path"


class CommunityDocumentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CommunityDocument model.
    """

    list_display = (
        "title",
        "category_display",  # Custom method for category name/path
        "creator",
        "created_at",
        "updated_at",
        "get_document_link",  # Custom method to link to the file
    )

    # Filters allow narrowing down documents by category, creator, and dates
    list_filter = (
        "category",
        "creator",
        "created_at",
        "updated_at",
    )

    # Enables searching across document title, description, and related user/category names
    search_fields = (
        "title",
        "id_document",  # Search by file name
        "creator__username",
        "creator__email",
        "category__category_name",  # Search by the category's name
    )

    # Use raw ID input for the creator ForeignKey for efficiency
    raw_id_fields = ("creator",)

    # Fields that should not be editable in the admin form
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # Adds a date-based drilldown navigation for 'created_at'
    date_hierarchy = "created_at"

    # Organize fields into sections on the add/edit form
    fieldsets = (
        (
            "Document Details",
            {
                "fields": (
                    "title",
                    "category",
                    "id_document",
                )  # category and id_document are editable
            },
        ),
        ("Creator Information", {"fields": ("creator",)}),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Custom method to display category name, using its __str__ for full path
    def category_display(self, obj):
        return obj.category.__str__() if obj.category else "-"

    category_display.short_description = "Category"

    # Custom method to create a clickable link to the document file
    def get_document_link(self, obj):
        if obj.id_document and hasattr(obj.id_document, "url"):
            from django.utils.html import format_html

            return format_html(
                '<a href="{}" target="_blank">Download File</a>', obj.id_document.url
            )
        return "No file"

    get_document_link.short_description = "Document File"
    get_document_link.allow_tags = True  # Required for format_html to render as HTML


class NoticeAdmin(admin.ModelAdmin):
    # Customize the list display columns in the admin change list view
    list_display = (
        "title",
        "created_at",
        "updated_at",
        "image_thumbnail",  # Custom method to display image preview
    )

    # Add search fields to enable searching notices in the admin
    search_fields = (
        "title",
        "details",
    )

    # Add filters to filter notices in the admin sidebar
    list_filter = (
        "created_at",
        "updated_at",
    )

    # Fields that should not be editable directly through the admin form
    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview_for_form",  # Custom method for preview in form
    )

    # Customize the form layout in the admin add/change view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "details",
                )
            },
        ),
        (
            "Image Information",
            {
                "fields": (
                    "image",
                    "image_preview_for_form",
                ),  # Include image and its preview
                "description": "Upload an image for the notice. Current image will be shown below.",
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # Custom method to display a small thumbnail of the image in the list_display
    def image_thumbnail(self, obj):
        if obj.image:
            # Displays the image with a max height for better presentation
            return format_html(
                '<img src="{}" style="max-height: 50px; width: auto;" />', obj.image.url
            )
        return "No Image"

    image_thumbnail.short_description = "Image"  # Column header in list display
    image_thumbnail.allow_tags = True  # Required for format_html

    # Custom method to display the image preview within the admin form
    def image_preview_for_form(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; width: auto;" />',
                obj.image.url,
            )
        return "No Image Uploaded Yet"

    image_preview_for_form.short_description = "Current Image Preview"
    image_preview_for_form.allow_tags = True


admin.site.register(CommunityDocument, CommunityDocumentAdmin)
# admin.site.register(CommunityResource, CommunityResourceAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueComment, IssueCommentAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Residence, ResidenceAdmin)
# admin.site.register(Visitor, VisitorAdmin)

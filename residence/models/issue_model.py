from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Issue(models.Model):
    class IssueStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"

    class PriorityLevel(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=IssueStatus.choices, default=IssueStatus.OPEN
    )

    priority = models.CharField(
        max_length=10, choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM
    )
    image = models.ImageField(upload_to="issue_images/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    reported_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
        help_text="User assigned to resolve the issue. Must be an Officer or Guard.",
    )

    def clean(self):
        if self.assigned_to:
            valid_groups = {"Officer", "Guard"}
            user_groups = set(self.assigned_to.groups.values_list("name", flat=True))
            if not user_groups & valid_groups:
                raise ValidationError(
                    "Assigned user must be in Officer or Guard group."
                )

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    class Meta:
        ordering = ["-reported_date"]


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issue_comments",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.issue.title}"

    class Meta:
        ordering = ["-created_at"]

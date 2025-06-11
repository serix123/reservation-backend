from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DocumentCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        return f"{self.parent.category_name + ' > ' if self.parent else ''}{self.category_name}"


class CommunityDocument(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="uploaded_file",
        null=True,
    )
    title = models.CharField(max_length=50)
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        related_name="document_category",
        null=True,
    )
    id_document = models.FileField(
        upload_to="community_documents/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Community Document"
        verbose_name_plural = "Community Documents"

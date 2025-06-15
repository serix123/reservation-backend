from rest_framework import serializers
from residence.models import CommunityDocument, DocumentCategory


class DocumentCategorySerializer(serializers.ModelSerializer):
    # This will display the ID of the parent category for simplicity in writing.
    # If you want to nest the parent category object, you'd define another
    # serializer and use it here (e.g., parent = DocumentCategorySerializer(read_only=True)).
    # For subcategories, we can use a recursive serializer.

    # Recursive field to show subcategories nested within a parent
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = DocumentCategory
        fields = [
            "id",
            "category_name",
            "parent",
            "subcategories",
        ]  # 'parent' will show parent's ID
        read_only_fields = [
            "subcategories"
        ]  # Subcategories are computed, not directly set

    def get_subcategories(self, obj):
        # Only serialize direct children, avoid infinite recursion for deeply nested structures
        # You might want to limit depth or only show names here.
        # This currently fetches and serializes immediate children.
        return DocumentCategorySerializer(
            obj.subcategories.all(), many=True, context=self.context
        ).data


class CommunityDocumentSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.get_full_name", read_only=True)

    # Use the nested DocumentCategorySerializer for the 'category' field
    # This will display the category object (with name, parent, subcategories)
    category = DocumentCategorySerializer(read_only=True)

    # For writing (creating/updating CommunityDocument), you'll need 'category_id'
    # as you'll be setting the ForeignKey by its ID.
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentCategory.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CommunityDocument
        fields = [
            "id",
            "title",
            "category",
            "category_id",  # 'category' for read, 'category_id' for write
            "id_document",
            "creator",
            "creator_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "creator", "creator_name", "created_at", "updated_at"]


class CreateCommunityDocumentSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Use the nested DocumentCategorySerializer for the 'category' field
    # This will display the category object (with name, parent, subcategories)
    category = DocumentCategorySerializer(read_only=True)

    # For writing (creating/updating CommunityDocument), you'll need 'category_id'
    # as you'll be setting the ForeignKey by its ID.
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentCategory.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CommunityDocument
        fields = [
            "id",
            "title",
            "category",
            "category_id",  # category can be set by ID
            "id_document",
            "creator",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

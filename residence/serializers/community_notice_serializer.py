from rest_framework import serializers
from residence.models import Notice  # Import your Notice model


class NoticeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Notice
        fields = ["id", "title", "details", "image", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

from rest_framework import serializers
from residence.models import Issue, IssueComment


class IssueSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "image",
            "user",
            "user_full_name",
            "reported_date",
            "resolved_date",
        ]
        read_only_fields = [
            "reported_date",
        ]


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "image",
            "user",
            "reported_date",
            "resolved_date",
        ]
        read_only_fields = [
            "id",
            "user",
            "reported_date",
            "resolved_date",
        ]


class ResolveIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = []  # No fields needed, just status change


class IssueCommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = IssueComment
        fields = [
            "id",
            "issue",
            "user",
            "user_full_name",
            "user_email",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at", "user_email"]

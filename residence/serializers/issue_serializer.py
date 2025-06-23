from django.contrib.auth import get_user_model
from rest_framework import serializers
from residence.models import Issue, IssueComment, Residence

User = get_user_model()


class IssueSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to_full_name = serializers.CharField(
        source="assigned_to.get_full_name", read_only=True
    )

    # Used only for write operations
    assigned_residence_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

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
            "assigned_to",
            "assigned_to_full_name",
            "assigned_residence_id",  # used only during create/update
            "reported_date",
            "resolved_date",
        ]
        read_only_fields = [
            "id",
            "user",
            "user_full_name",
            "assigned_to",
            "assigned_to_full_name",
            "reported_date",
            "resolved_date",
        ]

    def validate_assigned_residence_id(self, value):
        if value is None:
            return None
        try:
            residence = Residence.objects.get(id=value)
        except Residence.DoesNotExist:
            raise serializers.ValidationError("Residence not found.")
        if residence.role not in ["Officer", "Guard"]:
            raise serializers.ValidationError("Only Officer or Guard can be assigned.")
        return residence

    def create(self, validated_data):
        residence = validated_data.pop("assigned_residence_id", None)
        if residence:
            validated_data["assigned_to"] = residence.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        residence = validated_data.pop("assigned_residence_id", None)
        if residence:
            validated_data["assigned_to"] = residence.user
        return super().update(instance, validated_data)


class CreateIssueSerializer(serializers.ModelSerializer):
    assigned_residence_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

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
            "assigned_to",
            "reported_date",
            "resolved_date",
        ]
        read_only_fields = [
            "id",
            "user",
            "reported_date",
            "resolved_date",
        ]

        def validate_assigned_to(self, value):
            if value is None:
                return value
            group_names = value.groups.values_list("name", flat=True)
            if not any(name in ["Officer", "Guard"] for name in group_names):
                raise serializers.ValidationError(
                    "User must be in Officer or Guard group."
                )
            return value


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

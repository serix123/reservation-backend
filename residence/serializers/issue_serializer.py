from rest_framework import serializers
from residence.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(
        source='resident.user.get_full_name',
        read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'status',
            'resident',
            'resident_name',
            'reported_date',
            'resolved_date'
        ]
        read_only_fields = [
            'resident_name',
            'reported_date',
            'resolved_date'
        ]


class CreateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'description']


class ResolveIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = []  # No fields needed, just status change

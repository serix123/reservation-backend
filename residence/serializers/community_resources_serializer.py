# community/serializers.py
from rest_framework import serializers
from authentication.models import User
from residence.models import CommunityResource
from residence.serializers import ResidenceUserSerializer


class CommunityResourceSerializer(serializers.ModelSerializer):
    managed_by = ResidenceUserSerializer(read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='managed_by',
        write_only=True,
        required=False
    )

    class Meta:
        model = CommunityResource
        fields = [
            'id',
            'name',
            'description',
            'contact_info',
            'resource_type',
            'status',
            'managed_by',
            'manager_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'managed_by']

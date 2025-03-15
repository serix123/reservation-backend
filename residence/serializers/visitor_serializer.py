from rest_framework import serializers
from residence.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(
        source='residence.user.get_full_name',
        read_only=True
    )

    class Meta:
        model = Visitor
        fields = [
            'id',
            'name',
            'resident_name',
            'visit_date',
            'visit_purpose',
            'status',
            'check_in_time',
            'check_out_time',
            'residence',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            # 'status',
            'check_in_time',
            'check_out_time',
            'created_at',
            'updated_at'
        ]


class CreateVisitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitor
        fields = ['name', 'visit_date', 'visit_purpose']

    # def validate_status(self, value):
    #     if value not in [Visitor.Status.APPROVED, Visitor.Status.REJECTED]:
    #         raise serializers.ValidationError("Invalid status")
    #     return value

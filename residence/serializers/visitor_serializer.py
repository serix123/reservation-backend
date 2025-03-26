from django.utils import timezone
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


class SecurityCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['name', 'visit_purpose']
        read_only_fields = ['visit_date']  # Will be set in create()

    def create(self, validated_data):
        # Get the security staff user from request context
        user = self.context['request'].user

        # Create visitor with all required fields
        visitor = Visitor.objects.create(
            name=validated_data['name'],
            visit_purpose=validated_data['visit_purpose'],
            visit_date=timezone.now(),  # Auto-set current time
            residence=user.residence,  # Auto-assign to security staff's residence
            status=Visitor.VisitStatus.CHECKED_IN,
            check_in_time=timezone.now()
        )
        return visitor

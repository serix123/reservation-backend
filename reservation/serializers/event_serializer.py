from rest_framework import serializers

# import recurrence.serializers
from reservation.models import Event


class EventSerializer(serializers.ModelSerializer):

    # recurrence = recurrence.serializers.RecurrenceField()

    class Meta:
        model = Event
        fields = "__all__"

    # def get_approval_status(self, obj):
    #     return obj.approval.status if hasattr(obj, 'approval') else 'Not Available'

    # def get_approver_name(self, obj):
    #     return obj.approval.approver.name if hasattr(obj, 'approval') else 'None'

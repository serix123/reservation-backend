from rest_framework import serializers
from reservation.models import Notification
from reservation.serializers import EventSerializer


class NotificationSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'event', 'created_at']

    # def get_event_details(self, obj):
    #     if obj.event:
    #         return {
    #             'id': obj.event.id,
    #             'event_name': obj.event.event_name,
    #             'event_description': obj.event.event_description,
    #             'start_time': obj.event.start_time,
    #             'end_time': obj.event.end_time,
    #             'equipments': obj.event.equipments,
    #             'status': obj.event.status,
    #             'additional_needs': obj.event.additional_needs,
    #         }
    #     return None

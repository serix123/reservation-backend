from rest_framework import serializers

# import recurrence.serializers
from reservation.models import Event


class EventSerializer(serializers.ModelSerializer):

    # recurrence = recurrence.serializers.RecurrenceField()

    class Meta:
        model = Event
        fields = "__all__"

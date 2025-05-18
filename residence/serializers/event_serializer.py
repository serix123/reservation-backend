from rest_framework import serializers
from residence.models import Event
from authentication.models import User


class EventSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.get_full_name", read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "details",
            "location",
            "creator",
            "creator_name",
            "attendees_count",
            "is_attending",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "creator",
            "creator_name",
            "attendees_count",
            "is_attending",
            "created_at",
            "updated_at",
        ]

    def get_is_attending(self, obj):
        user = self.context["request"].user
        return user.is_authenticated and user in obj.attendees.all()


class CreateEventSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.get_full_name", read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = Event
        # fields = ['name', 'date', 'details', 'location']
        fields = [
            "id",
            "name",
            "date",
            "details",
            "location",
            "creator",
            "creator_name",
            "attendees_count",
            "is_attending",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "creator",
            "creator_name",
            "attendees_count",
            "is_attending",
            "created_at",
            "updated_at",
        ]

    def get_is_attending(self, obj):
        user = self.context["request"].user
        return user.is_authenticated and user in obj.attendees.all()


class AttendEventSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["attend", "unattend"])

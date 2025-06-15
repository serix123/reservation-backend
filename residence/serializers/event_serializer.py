from django.contrib.auth import get_user_model
from rest_framework import serializers
from residence.models import Event
from residence.permissions import IsOfficer

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.get_full_name", read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    is_attending = serializers.SerializerMethodField()

    # We will conditionally add 'attendees_list' in to_representation
    # attendees_list = serializers.StringRelatedField(many=True, read_only=True) # Could predefine but easier to add dynamically

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "status",
            "image",
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
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user.residence in obj.attendees.all()
        return False

    def to_representation(self, instance):
        """
        Dynamically adds 'attendees_list' field if the requesting user is an Officer.
        """
        representation = super().to_representation(instance)
        request = self.context.get("request")

        # Check if the user is an Officer using the custom permission class
        # Note: We pass the request to has_permission for proper context.
        if IsOfficer().has_permission(request, self.context.get("view")):
            # If the user is an Officer, add the list of attendee usernames/full names
            # You might want to use a nested serializer for more attendee details
            representation["attendees_list"] = [
                {
                    "full_name": attendee.user.get_full_name(),
                    "email": attendee.user.email,
                    "contact_number": attendee.contact_number,
                }
                for attendee in instance.attendees.all()
                if hasattr(attendee, "user")
            ]
        return representation


class CreateEventSerializer(serializers.ModelSerializer):
    # creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_name = serializers.CharField(source="creator.get_full_name", read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    is_attending = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "status",
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
            "status",
            "attendees_count",
            "creator",
            "creator_name",
            "is_attending",
            "created_at",
            "updated_at",
        ]

    def get_is_attending(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user == obj.creator
        return False


class AttendEventSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["attend", "unattend"])


class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[Event.EventStatus.CONFIRMED, Event.EventStatus.REJECTED],
        required=True,
        help_text="Set event status to 'confirmed' or 'rejected'.",
    )

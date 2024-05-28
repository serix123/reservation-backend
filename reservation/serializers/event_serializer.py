from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# import recurrence.serializers
from reservation.models import Approval, Department, Employee, Event, EventEquipment, Notification


class EventEquipmentSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(
        source="equipment.equipment_name")

    class Meta:
        model = EventEquipment
        fields = ["equipment", "equipment_name", "quantity"]


class EventSerializer(serializers.ModelSerializer):

    equipments = EventEquipmentSerializer(
        source="eventequipment_set", many=True, required=False
    )

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )

    class Meta:
        model = Event
        fields = [
            #   'requesitioner',
            "id",
            "requesitioner",
            "slip_number",
            "event_name",
            "event_description",
            "department",
            "contact_number",
            "additional_needs",
            "reserved_facility",
            "participants_quantity",
            "start_time",
            "end_time",
            "equipments",
            "status",
            "event_file",
        ]
        extra_kwargs = {
            "event_name": {"required": False, "allow_null": True},
            "reserved_facility": {"required": False, "allow_null": True},
            "start_time": {"required": False, "allow_null": True},
            "end_time": {"required": False, "allow_null": True},
            "equipments": {"required": False, "allow_null": True},
            "slip_number": {"required": False, "allow_null": True},
            "requesitioner": {"required": False, "allow_null": True},
        }

    def validate_event_file(self, value):
        if value is not None and not value.name.endswith(
            (".jpg", ".jpeg", ".png", ".pdf")
        ):
            raise serializers.ValidationError(
                "Unsupported file format. Only JPG, JPEG, PNG, and PDF are allowed."
            )
        return value

    def validate(self, data):
        current_time = datetime.now()

        if "start_time" in data and "end_time" in data:

            if data["start_time"].date() <= current_time.date():
                raise serializers.ValidationError({
                    'start_time': 'Start time must be a future date.'
                })

            if data["end_time"].date() <= current_time.date():
                raise serializers.ValidationError({
                    'end_time': 'End time must be a future date.'
                })

            if data["start_time"] >= data["end_time"]:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after the start time.'
                })

            if data["start_time"] > data["end_time"]:
                raise serializers.ValidationError(
                    "End time must be after start time.")
            # if data['start_time'] == data['end_time']:
            #     raise serializers.ValidationError(
            #         "Start time and end time cannot be the same.")
        # Check for existing events with 'confirmed' status and the same facility
        if (
            "reserved_facility" in data
            and "status" in data
            and data["status"] == "application"
        ):
            reserved_facility = data["reserved_facility"]
            overlapping_events = Event.objects.filter(
                reserved_facility=reserved_facility,
                status="confirmed",
                start_time__lt=data["end_time"],
                end_time__gt=data["start_time"],
            )
            if overlapping_events.exists():
                raise serializers.ValidationError(
                    "There is already a confirmed event at the same facility during the given time."
                )
        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Access the user from the serializer's context (if it's an update operation)
                user = self.context["request"].user
                employee = Employee.objects.get(user=user)
                equipments_data = validated_data.pop("eventequipment_set", [])
                event = Event.objects.create(
                    requesitioner=employee, **validated_data)

                for equipment_data in equipments_data:
                    EventEquipment.objects.create(
                        event=event, **equipment_data)

                status = validated_data.pop("status", {})
                if status == "application":

                    person_in_charge_status = 0
                    admin_status = 0
                    person_in_charge = event.reserved_facility.person_in_charge
                    if employee == person_in_charge:
                        person_in_charge_status = 1
                    if employee.is_admin:
                        admin_status = 1

                    Approval.objects.create(
                        event=event,
                        immediate_head_approver=employee.immediate_head,
                        person_in_charge_approver=event.reserved_facility.person_in_charge,
                        requesitioner=employee,
                        slip_number=event.slip_number,
                        person_in_charge_status=person_in_charge_status,
                        admin_status=admin_status,
                        # Default status
                        # status='pending'
                    )
                    message = f"An Approval request({event.slip_number}) has been made."
                    Notification.objects.create(
                        recipient=employee,  # Assuming requester has a user associated
                        message=message,
                        event=event,
                    )
                    Notification.objects.create(
                        # Assuming requester has a user associated
                        recipient=event.reserved_facility.person_in_charge,
                        message=message,
                        event=event,
                    )
                    Notification.objects.create(
                        recipient=employee.immediate_head,  # Assuming requester has a user associated
                        message=message,
                        event=event,
                    )
                    admins = Employee.objects.filter(is_admin=True)
                    # Loop through each admin and create a notification
                    for admin in admins:
                        Notification.objects.create(
                            recipient=admin,
                            message=message,
                            event=event
                        )

            return event
        except Exception as e:
            # Handle specific error, e.g., insufficient equipment quantity
            raise ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.event_name = validated_data.get(
                    "event_name", instance.event_name
                )
                instance.start_time = validated_data.get(
                    "start_time", instance.start_time
                )
                instance.end_time = validated_data.get(
                    "end_time", instance.end_time)
                # Handle the equipment data:
                instance.eventequipment_set.all().delete()
                # for event_equipment in event_equipments:
                #     equipment = event_equipment.equipment
                #     equipment.quantity_available += event_equipment.quantity
                #     equipment.save()
                equipments_data = validated_data.pop("eventequipment_set", [])
                for equipment_data in equipments_data:
                    eq_id = equipment_data.get("equipment").id
                    try:
                        event_eq = EventEquipment.objects.get(
                            event=instance, equipment_id=eq_id
                        )
                    except EventEquipment.DoesNotExist:
                        event_eq = EventEquipment.objects.create(
                            event=instance, **equipment_data
                        )
                    event_eq.quantity = equipment_data.get(
                        "quantity", event_eq.quantity
                    )
                    event_eq.save()

                status = validated_data.get("status")
                if instance.status != "application" and status == "application":
                    instance.status = status
                    instance.save()
                    # Create approval after the status update
                    user = self.context.get("user", None)
                    employee = Employee.objects.get(user=user)

                    person_in_charge_status = 0
                    admin_status = 0
                    person_in_charge = instance.reserved_facility.person_in_charge
                    if employee == person_in_charge:
                        person_in_charge_status = 1
                    if employee.is_admin:
                        admin_status = 1

                    if user is not None:
                        message = "An Approval request has been made"
                        Approval.objects.create(
                            event=instance,
                            requesitioner=employee,
                            immediate_head_approver=employee.immediate_head,
                            person_in_charge_approver=instance.reserved_facility.person_in_charge,
                            slip_number=instance.slip_number,
                            person_in_charge_status=person_in_charge_status,
                            admin_status=admin_status,
                        )
                        Notification.objects.create(
                            recipient=employee,  # Assuming requester has a user associated
                            message=message,
                            event=instance,
                        )
                elif instance.status == "application" and status == "draft":
                    instance.status = status
                    instance.save()
                    slip_number = validated_data.get("slip_number")
                    approval = Approval.objects.get(
                        slip_number=slip_number,
                        event=instance,
                    )
                    approval.delete()
                    message = "An Approval request has been deleted"
                    Notification.objects.create(
                        recipient=employee,  # Assuming requester has a user associated
                        message=message,
                        event=instance,
                    )
                else:
                    instance.save()
                return instance
        except Exception as e:
            # Handle specific error, e.g., insufficient equipment quantity
            raise ValidationError({"error": str(e)})

    # recurrence = recurrence.serializers.RecurrenceField()

    # def get_approval_status(self, obj):
    #     return obj.approval.status if hasattr(obj, 'approval') else 'Not Available'

    # def get_approver_name(self, obj):
    #     return obj.approval.approver.name if hasattr(obj, 'approval') else 'None'

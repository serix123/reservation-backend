from rest_framework import serializers

# import recurrence.serializers
from reservation.models import Approval, Employee, Event, EventEquipment


class EventEquipmentSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(
        source='equipment.equipment_name')

    class Meta:
        model = EventEquipment
        fields = ['equipment', 'equipment_name', 'quantity']


class EventSerializer(serializers.ModelSerializer):

    equipments = EventEquipmentSerializer(
        source='eventequipment_set', many=True, required=False)

    class Meta:
        model = Event
        fields = ['id',
                  #   'requesitioner',
                  'equipments',
                  'event_name', 'reserved_facility',
                  'start_time', 'end_time',
                  'status']
        extra_kwargs = {
            'event_name': {'required': False, 'allow_null': True},
            'reserved_facility': {'required': False, 'allow_null': True},
            'start_time': {'required': False, 'allow_null': True},
            'end_time': {'required': False, 'allow_null': True},
            'equipments': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] > data['end_time']:
                raise serializers.ValidationError(
                    "End time must be after start time.")
            # if data['start_time'] == data['end_time']:
            #     raise serializers.ValidationError(
            #         "Start time and end time cannot be the same.")
        return data

    def create(self, validated_data):
        # Access the user from the serializer's context (if it's an update operation)
        user = self.context['request'].user
        employee = Employee.objects.get(user=user)
        equipments_data = validated_data.pop('eventequipment_set', [])
        event = Event.objects.create(requesitioner=employee, **validated_data)
        print(f'{validated_data}')

        for equipment_data in equipments_data:
            EventEquipment.objects.create(event=event, **equipment_data)

        status = validated_data.pop('status', {})
        if status == "application":
            Approval.objects.create(
                event=event,
                immediate_head_approver=employee.immediate_head,
                person_in_charge_approver=event.reserved_facility.person_in_charge,
                requesitioner=employee,
                # Default status
                # status='pending'
            )
        return event

    def update(self, instance, validated_data):
        instance.event_name = validated_data.get(
            'event_name', instance.event_name)
        instance.start_time = validated_data.get(
            'start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        # Handle the equipment data:
        equipments_data = validated_data.pop('eventequipment_set', [])
        for equipment_data in equipments_data:
            eq_id = equipment_data.get('equipment').id
            event_eq = EventEquipment.objects.get(
                event=instance, equipment_id=eq_id)
            event_eq.quantity = equipment_data.get(
                'quantity', event_eq.quantity)
            event_eq.save()

        status = validated_data.get('status')
        if instance.status != 'application' and status == 'application':
            instance.status = status
            instance.save()
            # Create approval after the status update
            user = self.context['request'].user
            employee = Employee.objects.get(user=user)
            Approval.objects.create(
                event=instance,
                requesitioner=employee,
                immediate_head_approver=employee.immediate_head,
                person_in_charge_approver=instance.reserved_facility.person_in_charge,
            )
        else:
            instance.save()
        return instance
    # recurrence = recurrence.serializers.RecurrenceField()

    # def get_approval_status(self, obj):
    #     return obj.approval.status if hasattr(obj, 'approval') else 'Not Available'

    # def get_approver_name(self, obj):
    #     return obj.approval.approver.name if hasattr(obj, 'approval') else 'None'

import uuid
from django.db import models, transaction
from reservation.models.department_model import Department
from reservation.models.employee_model import Employee
from reservation.models.equipment_model import Equipment
from reservation.models.facility_model import Facility


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.TextField(blank=True, null=True)
    requesitioner = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="events"
    )
    contact_number = models.CharField(max_length=11, blank=True, null=True)
    reserved_facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="events"
    )
    participants_quantity = models.PositiveIntegerField(default=0)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # equipment = models.ManyToManyField(
    #     Equipment, blank=True, related_name="events")
    equipments = models.ManyToManyField(Equipment, through="EventEquipment", blank=True)
    STATUS_TYPE = (
        ("application", "Application"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("returned", "Returned"),
        ("draft", "Draft"),
    )
    status = models.CharField(max_length=12, choices=STATUS_TYPE, default="draft")
    additional_needs = models.TextField(blank=True, null=True)
    slip_number = models.CharField(max_length=20, unique=True, blank=True)
    event_file = models.FileField(
        upload_to="event_files/",
        blank=True,
        null=True,
        help_text="Upload a PDF or JPEG file.",
    )
    # RECURRENCE_CHOICES = (
    #     ('none', 'None'),
    #     ('daily', 'Daily'),
    #     ('weekly', 'Weekly'),
    #     ('monthly', 'Monthly'),
    # )
    # recurrence = models.CharField(
    #     max_length=7, choices=RECURRENCE_CHOICES, default='none')
    # days_of_week = models.CharField(
    #     max_length=15, blank=True, null=True
    # )  # CSV like "1,3,5" for Mon, Wed, Fri

    # def get_weekday_display(self):
    #     weekdays = {
    #         "1": "Monday",
    #         "2": "Tuesday",
    #         "3": "Wednesday",
    #         "4": "Thursday",
    #         "5": "Friday",
    #         "6": "Saturday",
    #         "7": "Sunday",
    #     }
    #     days = (weekdays.get(day, "") for day in self.days_of_week.split(","))
    #     return ", ".join(filter(None, days))

    @property
    def requesitioner_name(self):
        return str(self.requesitioner)

    def cancel_event(self):
        """Cancels the event and deletes the associated approval."""
        with transaction.atomic():
            if hasattr(self, "approval"):
                self.approval.delete()  # Delete the associated Approval record
            if self.status == "confirmed":
                event_equipments = self.eventequipment_set.select_for_update().all()
                for event_equipment in event_equipments:
                    equipment = event_equipment.equipment
                    equipment.equipment_quantity += event_equipment.quantity
                    equipment.save()
            self.status = "cancelled"
            self.save()

    def update_event(self, status):
        if status == "confirmed":
            self.status = status
            self.update_equipment_inventory()
            self.save()
        elif status == "cancelled":
            self.delete()
        else:
            self.status = status
            self.save()

    def update_equipment_inventory(self):
        with transaction.atomic():  # Start of transaction
            for event_equipment in self.eventequipment_set.select_related(
                "equipment"
            ).select_for_update():
                # The select_related() call ensures that the related Equipment objects are also selected
                equipment = event_equipment.equipment
                new_quantity = equipment.equipment_quantity - event_equipment.quantity
                if new_quantity < 0:
                    raise ValueError("Insufficient equipment quantity to use.")
                equipment.equipment_quantity = new_quantity
                equipment.save(
                    update_fields=["equipment_quantity"]
                )  # Update only the quantity field

    def generate_slip_number(self):
        # Generate a unique slip number, which could be based on the current date/time or other logic
        # Example using UUID, shortened for simplicity
        return str(uuid.uuid4())[:8]

    def save(self, *args, **kwargs):
        if not self.slip_number:
            # Generate a unique slip number on first save
            self.slip_number = self.generate_slip_number()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Retrieve and update within a transaction
            event_equipments = self.eventequipment_set.select_for_update().all()
            for event_equipment in event_equipments:
                equipment = event_equipment.equipment
                equipment.equipment_quantity += event_equipment.quantity
                equipment.save()
            self.eventequipment_set.all().delete()
            if hasattr(self, "approval"):
                self.approval.delete()  # Delete the associated Approval record
            # Call the original delete method
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.event_name} ({self.status})"

    class Meta:
        ordering = ["event_name"]

    # def save(self, *args, **kwargs):
    #     if self.pk:  # Check if this is not a new instance
    #         old_status = Event.objects.get(pk=self.pk).status
    #         if old_status == 'draft' and self.status == 'application':
    #             super().save(*args, **kwargs)  # Save the event first
    #             # Create an associated approval
    #             Approval.objects.create(event=self, requesitioner=self.requesitioner)
    #         else:
    #             super().save(*args, **kwargs)
    #     else:
    #         super().save(*args, **kwargs)


class EventEquipment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.equipment.equipment_name} for {self.event.event_name}"


# class EventApplication(models.Model):

#     event_name = models.CharField(max_length=255)
#     event_description = models.TextField(blank=True, null=True)
#     requesitioner = models.ForeignKey(
#         Employee, on_delete=models.CASCADE, related_name="events"
#     )
#     reserved_facility = models.ForeignKey(
#         Facility, on_delete=models.CASCADE, related_name="events"
#     )
#     department = models.ForeignKey(
#         "Department",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="events",
#     )
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     # equipment = models.ManyToManyField(
#     #     Equipment, blank=True, related_name="events")
#     equipments = models.ManyToManyField(Equipment, through='EventEquipment')
#     STATUS_TYPE = (
#         ("application", "Application"),
#         ("confirmed", "Confirmed"),
#         ("cancelled", "Cancelled"),
#         ("returned", "Returned"),
#         ("draft", "Draft"),
#     )
#     status = models.CharField(
#         max_length=12, choices=STATUS_TYPE, default='draft')

#     additional_needs = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.event_name} ({self.status})"

#     def update_equipment_inventory(self):
#         for equipment in self.eventequipment_set.all():
#             equipment.equipment.equipment_quantity -= equipment.quantity
#             equipment.equipment.save()

#     def approve(self):
#         """Move the event application to the Event table upon approval."""
#         if self.status == 1:  # Ensure it's ready for approval
#             event = Event.objects.create(
#                 event_name=self.event_name,
#                 event_description=self.event_description,
#                 requesitioner=self.requesitioner,
#                 reserved_facility=self.reserved_facility,
#                 start_time=self.start_time,
#                 end_time=self.end_time,
#                 additional_needs=self.additional_needs,
#                 equipments=self.equipments,
#                 status="confirmed"
#             )
#             self.delete()  # Optionally delete the application or mark as transferred
#         return event

from django.db import models


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=100)
    EQUIPMENT_TYPE = (
        (1, "Logistics"),
        (2, "MIS"),
        (3, "Personnel"),
        (4, "Security"),
    )
    equipment_type = models.IntegerField(choices=EQUIPMENT_TYPE, default=1)
    equipment_quantity = models.PositiveIntegerField(default=0)
    WORK_CHOICES = (
        (1, "Setup only"),
        (2, "Dedicated"),
        (3, "Overtime"),
    )
    work_type = models.IntegerField(choices=WORK_CHOICES, null=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"

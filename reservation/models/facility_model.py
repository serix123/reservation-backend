from django.db import models

from reservation.models.department_model import Department
from reservation.models.employee_model import Employee


def get_default_department_id():
    from reservation.models import (
        Department,
    )  # Import inside function to avoid circular import issues

    default_department = Department.objects.first()
    if default_department:
        return default_department.id
    return None  # Ensure there is a sensible default, or handle this case properly!


def get_default_person_in_charge():
    from reservation.models import (
        Employee,
    )  # Import inside function to avoid circular import issues

    default_person_in_charge = Employee.objects.first()
    if default_person_in_charge:
        return default_person_in_charge.id
    return None  # Ensure there is a sensible default, or handle this case properly!


class Facility(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="facilities",
        null=True,
        default=get_default_department_id,
    )
    person_in_charge = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_facilities",
        default=get_default_person_in_charge,
    )

    def __str__(self):
        return self.name

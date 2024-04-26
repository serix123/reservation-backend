from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    superior = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_department",
    )

    def __str__(self):
        return self.name

from django.contrib import admin

from residence.models import (Residence)
# Register your models here.


class ResidenceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "role",
        "contact_number",
        "address",
        "registration_date",
    ]
    list_filter = ["role"]
    search_fields = ["first_name", "last_name", "role"]
    ordering = ["first_name", "last_name", "role"]


admin.site.register(Residence, ResidenceAdmin)

# Generated by Django 4.2.11 on 2024-05-03 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_remove_event_equipment_remove_event_recurrence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='equipments',
            field=models.ManyToManyField(blank=True, null=True, through='reservation.EventEquipment', to='reservation.equipment'),
        ),
    ]

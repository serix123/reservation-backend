# Generated by Django 4.2.11 on 2024-04-29 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_facility_department_alter_facility_person_in_charge_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=100)),
                ('equipment_type', models.CharField(max_length=100)),
                ('equipment_quantity', models.PositiveIntegerField(default=0)),
                ('work_type', models.IntegerField(choices=[(1, 'Setup only'), (2, 'Dedicated'), (3, 'Overtime')], default=1)),
            ],
        ),
    ]
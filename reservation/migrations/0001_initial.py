# Generated by Django 4.2.11 on 2024-05-03 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reservation.models.facility_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='first_name', max_length=100)),
                ('last_name', models.CharField(default='last_name', max_length=100)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.department')),
                ('immediate_head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='reservation.employee')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=100)),
                ('equipment_type', models.IntegerField(choices=[(1, 'Logistics'), (2, 'MIS'), (3, 'Personnel'), (4, 'Security')], default=1)),
                ('equipment_quantity', models.PositiveIntegerField(default=0)),
                ('work_type', models.IntegerField(blank=True, choices=[(1, 'Setup only'), (2, 'Dedicated'), (3, 'Overtime')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('department', models.ForeignKey(default=reservation.models.facility_model.get_default_department_id, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facilities', to='reservation.department')),
                ('person_in_charge', models.ForeignKey(default=reservation.models.facility_model.get_default_person_in_charge, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_facilities', to='reservation.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('event_description', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Cancelled'), (4, 'Denied'), (5, 'Draft')], default=5)),
                ('recurrence', models.CharField(choices=[('none', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='none', max_length=7)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='reservation.department')),
                ('equipment', models.ManyToManyField(blank=True, related_name='events', to='reservation.equipment')),
                ('requesitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reservation.employee')),
                ('reserved_facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='reservation.facility')),
            ],
            options={
                'ordering': ['event_name'],
            },
        ),
        migrations.AddField(
            model_name='department',
            name='immediate_head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_department', to='reservation.employee'),
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('immediate_head_approved', models.BooleanField(default=False)),
                ('person_in_charge_approved', models.BooleanField(default=False)),
                ('admin_approved', models.BooleanField(default=False)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='reservation.event')),
                ('requesitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='reservation.employee')),
            ],
        ),
    ]

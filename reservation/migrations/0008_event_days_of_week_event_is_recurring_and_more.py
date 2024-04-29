# Generated by Django 4.2.11 on 2024-04-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_event_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='days_of_week',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=255),
        ),
    ]
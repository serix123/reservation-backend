# Generated by Django 4.2.11 on 2024-05-04 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0012_event_participants_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contact_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
# Generated by Django 5.2.3 on 2025-07-11 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0002_alter_bookingperson_nationality'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='country',
        ),
    ]

# Generated by Django 3.2.7 on 2024-02-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0043_auto_20240208_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='available',
            new_name='is_available',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='room',
            name='unavailable',
        ),
        migrations.AddField(
            model_name='booking',
            name='checkin_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='checkout_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]

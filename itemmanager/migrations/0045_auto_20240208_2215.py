# Generated by Django 3.2.7 on 2024-02-08 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0044_auto_20240208_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='email',
        ),
        migrations.RemoveField(
            model_name='room',
            name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
        migrations.AddField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
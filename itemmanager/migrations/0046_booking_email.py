# Generated by Django 3.2.7 on 2024-02-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0045_auto_20240208_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]

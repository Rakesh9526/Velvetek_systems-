# Generated by Django 5.1.3 on 2024-12-20 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0042_currentstatus_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelcharge',
            name='customer_name',
            field=models.CharField(default=0, max_length=225),
        ),
        migrations.AddField(
            model_name='fuelcharge',
            name='issue',
            field=models.TextField(default=0),
        ),
    ]

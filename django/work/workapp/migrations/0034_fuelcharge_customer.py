# Generated by Django 5.1.3 on 2024-12-12 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0033_remove_fuelcharge_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelcharge',
            name='customer',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='workapp.apply'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0035_remove_fuelcharge_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelcharge',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

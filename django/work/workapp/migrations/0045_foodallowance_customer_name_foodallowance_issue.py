# Generated by Django 5.1.3 on 2024-12-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0044_alter_fuelcharge_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodallowance',
            name='customer_name',
            field=models.CharField(default=True, max_length=225),
        ),
        migrations.AddField(
            model_name='foodallowance',
            name='issue',
            field=models.TextField(default=True),
        ),
    ]

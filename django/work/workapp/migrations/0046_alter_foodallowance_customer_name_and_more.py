# Generated by Django 5.1.3 on 2024-12-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0045_foodallowance_customer_name_foodallowance_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodallowance',
            name='customer_name',
            field=models.CharField(max_length=225),
        ),
        migrations.AlterField(
            model_name='foodallowance',
            name='issue',
            field=models.TextField(),
        ),
    ]
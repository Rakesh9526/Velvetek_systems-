# Generated by Django 5.1.3 on 2024-12-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0019_alter_apply_service_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='service_by',
            field=models.CharField(max_length=225),
        ),
    ]

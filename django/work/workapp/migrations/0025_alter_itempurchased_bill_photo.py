# Generated by Django 5.1.3 on 2024-12-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0024_alter_apply_service_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempurchased',
            name='bill_photo',
            field=models.ImageField(upload_to='itempurchased'),
        ),
    ]

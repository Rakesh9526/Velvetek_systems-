# Generated by Django 5.1.3 on 2024-12-19 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0039_itempurchased_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorinfo',
            name='apply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_infos', to='workapp.apply'),
        ),
    ]
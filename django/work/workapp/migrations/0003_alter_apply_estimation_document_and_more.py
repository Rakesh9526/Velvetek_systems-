# Generated by Django 5.1.3 on 2024-11-20 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0002_apply_estimation_document_apply_issue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='estimation_document',
            field=models.FileField(blank=True, null=True, upload_to='apply'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='item_name_or_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='apply',
            name='photos_of_item',
            field=models.ImageField(blank=True, null=True, upload_to='apply'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='reffered_by',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

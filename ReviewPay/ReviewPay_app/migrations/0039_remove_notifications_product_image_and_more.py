# Generated by Django 4.2.16 on 2025-06-16 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0038_businessdetail_created_at_businessdetail_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='product_image',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='product_image_date',
        ),
    ]

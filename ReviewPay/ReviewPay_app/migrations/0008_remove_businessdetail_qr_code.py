# Generated by Django 4.2.16 on 2025-04-04 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0007_businessdetail_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessdetail',
            name='qr_code',
        ),
    ]

# Generated by Django 4.2.16 on 2025-05-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0029_usersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='duration',
            field=models.DurationField(),
        ),
    ]

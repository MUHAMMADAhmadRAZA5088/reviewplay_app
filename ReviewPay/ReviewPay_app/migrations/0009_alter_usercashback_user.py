# Generated by Django 4.2.16 on 2025-02-06 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0008_alter_usercashback_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercashback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercashback', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.16 on 2025-04-24 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0017_remove_businessdetail_business_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcome_new_user',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='new_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

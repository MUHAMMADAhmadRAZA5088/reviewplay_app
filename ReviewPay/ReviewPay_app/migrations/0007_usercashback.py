# Generated by Django 4.2.16 on 2025-02-06 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0006_referralcashback_business_reviewcashback_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCashBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_id', models.IntegerField()),
                ('invoice_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercashback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

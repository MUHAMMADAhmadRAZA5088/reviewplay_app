# Generated by Django 4.2.16 on 2024-12-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewPay_app', '0006_delete_emailvalidation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='business',
        ),
        migrations.RemoveField(
            model_name='uploadedimages',
            name='business',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='abn_number',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='businessLogo',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='business_address',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='business_name',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='category',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='name',
        ),
        migrations.RemoveField(
            model_name='categoryusers',
            name='sub_category',
        ),
        migrations.AlterField(
            model_name='categoryusers',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('business', 'Business User')], default='admin user', max_length=10),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='UploadedImages',
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-13 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_coupon_expiry_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='expiry_date',
            new_name='end_date',
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-11 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.DeleteModel(
            name='Referral',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]

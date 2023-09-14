# Generated by Django 4.2.4 on 2023-09-09 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_offer'),
        ('order', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.productvariant'),
            preserve_default=False,
        ),
    ]
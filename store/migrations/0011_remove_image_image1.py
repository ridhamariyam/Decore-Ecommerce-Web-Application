# Generated by Django 4.2.4 on 2023-09-16 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_image_image1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image1',
        ),
    ]

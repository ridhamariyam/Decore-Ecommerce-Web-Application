# Generated by Django 4.2.4 on 2023-08-22 11:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('cart_image', models.ImageField(blank=True, upload_to='photos/categories')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]

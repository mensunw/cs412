# Generated by Django 5.1.2 on 2024-10-18 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0005_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image_url',
            field=models.URLField(blank=True),
        ),
    ]
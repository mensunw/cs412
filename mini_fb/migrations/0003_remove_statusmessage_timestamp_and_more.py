# Generated by Django 5.1.1 on 2024-10-12 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_statusmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusmessage',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='statusmessage',
            name='published',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
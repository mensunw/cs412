# Generated by Django 5.1.3 on 2024-12-09 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_remove_feedbackresponse_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='stars',
            field=models.TextField(default=3),
            preserve_default=False,
        ),
    ]

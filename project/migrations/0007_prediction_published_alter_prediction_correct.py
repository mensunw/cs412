# Generated by Django 5.1.3 on 2024-12-10 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_feedback_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='published',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='correct',
            field=models.BooleanField(blank=True),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-09 01:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_remove_game_kill_ratio_delete_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackresponse',
            name='rating',
            field=models.TextField(default='4'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0002_alter_playlist_duration_alter_playlist_songs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="duration",
            field=models.IntegerField(verbose_name="Duration (ms)"),
        ),
    ]
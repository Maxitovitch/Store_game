# Generated by Django 5.0.6 on 2024-09-07 16:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop_game", "0005_remove_supportticket_subject_supportticket_game_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="supportticket",
            unique_together={("user", "game")},
        ),
    ]

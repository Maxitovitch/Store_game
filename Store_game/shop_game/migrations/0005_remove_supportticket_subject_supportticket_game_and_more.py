# Generated by Django 5.0.6 on 2024-09-07 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop_game", "0004_alter_systemrequirement_game"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="supportticket",
            name="subject",
        ),
        migrations.AddField(
            model_name="supportticket",
            name="game",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop_game.game",
                verbose_name="Игра",
            ),
        ),
        migrations.AddField(
            model_name="supportticket",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="support_tickets",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="description",
            field=models.TextField(verbose_name="Описание игры"),
        ),
        migrations.AlterField(
            model_name="game",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="games",
                to="shop_game.genre",
                verbose_name="Жанр игры",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="image",
            field=models.ImageField(
                blank=True,
                default="game/images/default.png",
                help_text="800x990px",
                null=True,
                upload_to="game/images/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Цена игры"
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Название игры"),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Название жанра"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="user/avatars/default_avatar.png",
                null=True,
                upload_to="user/avatars/",
                verbose_name="Аватар",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="money",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=20, verbose_name="Баланс"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="vote_type",
            field=models.CharField(
                choices=[("like", "Like"), ("dislike", "Dislike")],
                max_length=10,
                verbose_name="Тип оценки",
            ),
        ),
        migrations.AlterField(
            model_name="supportticket",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Время создания"
            ),
        ),
        migrations.AlterField(
            model_name="supportticket",
            name="email",
            field=models.EmailField(
                max_length=254, verbose_name="Электронная почта пользователя"
            ),
        ),
        migrations.AlterField(
            model_name="supportticket",
            name="message",
            field=models.TextField(verbose_name="Сообщение"),
        ),
        migrations.AlterField(
            model_name="systemrequirement",
            name="cpu",
            field=models.CharField(
                blank=True,
                default="Не указано",
                max_length=100,
                verbose_name="Процессор",
            ),
        ),
        migrations.AlterField(
            model_name="systemrequirement",
            name="gpu",
            field=models.CharField(
                blank=True,
                default="Не указано",
                max_length=100,
                verbose_name="Видеокарта",
            ),
        ),
        migrations.AlterField(
            model_name="systemrequirement",
            name="os",
            field=models.CharField(
                blank=True,
                default="Не указано",
                max_length=100,
                verbose_name="Операционная система",
            ),
        ),
        migrations.AlterField(
            model_name="systemrequirement",
            name="ram",
            field=models.CharField(
                blank=True, default="Не указано", max_length=50, verbose_name="ОЗУ"
            ),
        ),
        migrations.AlterField(
            model_name="systemrequirement",
            name="storage",
            field=models.CharField(
                blank=True,
                default="Не указано",
                max_length=50,
                verbose_name="Место на диске",
            ),
        ),
    ]

import string
from random import choices
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='user/avatars/', null=True, blank=True, default='user/avatars/default_avatar.png', verbose_name='Аватар')
    money = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='Баланс', blank=True)

    def __str__(self):
        return self.user.username

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название жанра', blank=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название игры', blank=True)
    description = models.TextField(verbose_name='Описание игры', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена игры', blank=True)
    genre = models.ForeignKey('Genre', related_name='games', on_delete=models.CASCADE, verbose_name='Жанр игры', blank=True)
    image = models.ImageField(upload_to='game/images/', null=True, blank=True, help_text='800x990px', verbose_name='Изображение', default='game/images/default.png')

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        SystemRequirement.objects.get_or_create(
            game=self,
            os='Не указано',
            cpu='Не указано',
            ram='Не указано',
            storage='Не указано',
            gpu='Не указано'
        )

class SystemRequirement(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра', related_name='system_requirements', blank=True)
    os = models.CharField(max_length=100, verbose_name='Операционная система', blank=True, default='Не указано')
    cpu = models.CharField(max_length=100, verbose_name='Процессор', blank=True, default='Не указано')
    ram = models.CharField(max_length=50, verbose_name='ОЗУ', blank=True, default='Не указано')
    storage = models.CharField(max_length=50, verbose_name='Место на диске', blank=True, default='Не указано')
    gpu = models.CharField(max_length=100, blank=True, verbose_name='Видеокарта', default='Не указано')

    def __str__(self):
        return f'Системные требования для {self.game}'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)
    vote_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')], verbose_name='Тип оценки', blank=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f'Рейтинг игры {self.game.title}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)
    def generate_code(self):
        code = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
        while Order.objects.filter(code=code).exists():
            code = ''.join(choices(string.ascii_uppercase + string.digits, k=10))
        return code

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets', null=True, blank=True, verbose_name='Пользователь')
    subject = models.CharField(max_length=100, verbose_name='Тема', blank=True)
    email = models.EmailField(verbose_name='Электронная почта пользователя', blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, verbose_name='Игра', null=True)
    message = models.TextField(verbose_name='Сообщение', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'Сообщение от {self.user} в {self.created_at}'

    class Meta:
        unique_together = ('user', 'game')


from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        help_text='Укажите логин',
        max_length=150,
        unique=True,
        validators=(validate_username,),
        error_messages={'unique': 'Этот никнейм уже занят!'}
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        max_length=254,
        unique=True,
        error_messages={'unique': 'Этот email уже зарегистрирован!'}
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Укажите имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Укажите фамилию',
        max_length=150,
    )
    password = models.CharField(
        verbose_name='Пароль',
        help_text='Обязательное поле, не более 150 символов',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_username'
            ),
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        help_text='Подписчик на автора рецепта',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепата',
        help_text='Автор рецепта, на которого подписываются',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user!=author',
            ),
        )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """ Модель тэгов созданных рецептов. """
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Введите название тэга',
    )
    color = models.CharField(max_length=7, unique=True, choices=COLOR_CHOICES,
                             verbose_name='Цвет в HEX')
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    """ Модель ингредиентов для рецептов."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите процесс приготовления рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Укажите ингрeдиенты',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Укажите теги',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления - 1 минута!'),
        )
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """ Количество ингредиентов в блюде."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингрeдиента',
        help_text='Укажите количество ингрeдиента',
        validators=(
            MinValueValidator(
                1, message='Количество не может быть меньше 1!'),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f' {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    """ Модель для избранных рецептов """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorites'
            ),
        )

    def __str__(self):
        return f'{self.recipe.name} - любимый рецепт {self.user}'


class Follow(models.Model):
    """ Модель подписок """

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


class ShoppingCart(models.Model):
    """ Модель покупок """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_recipe'
            ),
        )

    def __str__(self):
        return f'{self.user} положил в корзину {self.recipe}'


class TagInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'{self.tag.name} для рецепта {self.recipe.name}'

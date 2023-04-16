from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from users.models import User


class BaseTagIngredient(models.Model):
    name = models.CharField('Название', max_length=settings.LEN_TEXT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Ingredient(BaseTagIngredient):
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.LEN_TEXT
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(BaseTagIngredient):
    color = models.CharField('Цвет в HEX', max_length=7)
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=settings.LEN_TEXT,
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тэги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient', verbose_name='Ингредиенты'
    )
    image = models.ImageField(
        'Картинка',
    )
    name = models.CharField('Название', max_length=settings.LEN_TEXT)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки (в минутах)',
        validators=[MinValueValidator(1), ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField('Количество')


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_pair'),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_not_author'),
        ]


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик',
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор',
#     )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['user', 'author'], name='unique_pair'),
    #         models.CheckConstraint(
    #             check=~models.Q(user=models.F('author')),
    #             name='user_not_author'),
    #     ]

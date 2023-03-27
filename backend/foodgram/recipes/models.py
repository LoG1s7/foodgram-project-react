from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.SlugField('Название', max_length=200)
    measurment_unit = models.SlugField('Единица измерения', max_length=200)


class Tag(models.Model):
    pass


class Recipe(models.Model):
    ingredients = models.ForeignKey()
    tags = models.ForeignKey()
    image = models.ImageField(
        'Картинка',
    )
    name = models.SlugField('Название', max_length=200)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки (в минутах)',
        validators=[MinValueValidator(1), ]
    )


class Follow(models.Model):
    pass

import pytest


@pytest.fixture
def tag_1():
    from recipes.models import Tag
    return Tag.objects.create(
        name="tag_1", color="#008888", slug="tag_1")


@pytest.fixture
def tag_2():
    from recipes.models import Tag
    return Tag.objects.create(
        name="tag_2", color="#008000", slug="tag_2")


@pytest.fixture
def ingredient_1():
    from recipes.models import Ingredient
    return Ingredient.objects.create(
        name="ingredient_1", measurement_unit="г")


@pytest.fixture
def ingredient_2():
    from recipes.models import Ingredient
    return Ingredient.objects.create(
        name="ingredient_2", measurement_unit="кг")


@pytest.fixture
def recipe_1(ingredient_1, ingredient_2, user, tag_1, tag_2):
    from recipes.models import Recipe
    return Recipe.objects.create(
        author=user,
        ingredients=[ingredient_1, ingredient_2],
        tags=[tag_1, tag_2],
        image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        name='Рецепт_1',
        text='Описание рецепта_1',
        cooking_time=10,)


@pytest.fixture
def recipe_2(ingredient_2, user, tag_2):
    from recipes.models import Recipe
    return Recipe.objects.create(
        author=user,
        ingredients=[ingredient_2, ],
        tags=[tag_2, ],
        image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        name='Рецепт_2',
        text='Описание рецепта_2',
        cooking_time=20,)

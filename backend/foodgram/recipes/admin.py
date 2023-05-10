from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Subscribe, Tag)


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_classes = [TagResource]
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


# class RecipeIngredientResource(resources.ModelResource):
#     ingredient = Field(attribute='ingredient', column_name='ingredient_id',
#                        widget=ForeignKeyWidget(Ingredient))
#
#     class Meta:
#         model = RecipeIngredient
#         columns = ('id', 'ingredient_id', 'amount')
#
#
# class RecipeIngredientInline(admin.TabularInline):
#     model = RecipeIngredient
#
#
# class RecipeResource(resources.ModelResource):
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'tags', 'author', 'ingredients', 'image', 'name', 'text',
#             'cooking_time',
#         )
#
#
# @admin.register(Recipe)
# class RecipeAdmin(ImportExportModelAdmin):
#     resource_classes = [RecipeResource, RecipeIngredientResource]
#     list_display = ('id', 'author', 'image', 'name', 'text', 'cooking_time',)
#     inlines = (RecipeIngredientInline, )
#     search_fields = ('name',)
#     list_filter = ('name',)
#     empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    empty_value_display = '-пусто-'

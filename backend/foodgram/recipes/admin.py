from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from import_export.fields import Field
# from import_export.widgets import ForeignKeyWidget
from recipes.models import Ingredient, Recipe, Tag, Follow


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

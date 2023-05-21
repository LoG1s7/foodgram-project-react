from django_filters import rest_framework
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.NumberFilter(
        method='is_favorite_filter')
    is_in_shopping_cart = filters.NumberFilter(
        method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def is_favorite_filter(self, queryset, name, value):

        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):

        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

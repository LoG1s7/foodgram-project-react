from django_filters import filters, rest_framework

from recipes.models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    tag = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.NumberFilter(
        method='is_favorite_filter')
    is_in_shopping_cart = filters.NumberFilter(
        method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def is_favorite_filter(self, queryset, name, value):
        return Recipe.objects.filter(
            favorite__user=self.request.user)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return Recipe.objects.filter(
            cart__user=self.request.user)

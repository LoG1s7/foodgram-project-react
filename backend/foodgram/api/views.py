# from api.filters import TitleFilter
from api.permissions import RecipesPermission
# from api.serializers import
# from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (TagSerializer, IngredientSerializer,
                             RecipeSerializer, PostRecipeSerializer,
                             SubscribeSerializer, )
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK
from recipes.models import Ingredient, Recipe, Tag, Subscribe
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    search_fields = ('^name',)
    lookup_field = 'name'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          RecipesPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('get', 'list'):
            return RecipeSerializer
        return PostRecipeSerializer


class SubscribeViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = SubscribeSerializer
    # permission_classes = (IsAuthenticated, )
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('^following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


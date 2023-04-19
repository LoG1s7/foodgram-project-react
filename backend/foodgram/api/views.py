# from api.filters import TitleFilter
from api.permissions import RecipesPermission
# from api.serializers import
# from django.db import IntegrityError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (TagSerializer, IngredientSerializer,
                             RecipeSerializer, PostRecipeSerializer,
                             SubscribeSerializer, CustomUserSerializer,
                             FavoriteSerializer)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from recipes.models import Ingredient, Recipe, Tag, Subscribe, Favorite
from users.models import User
from djoser.views import UserViewSet


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
    permission_classes = (IsAuthenticatedOrReadOnly, RecipesPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('get', 'list'):
            return RecipeSerializer
        return PostRecipeSerializer

    @action(
        methods=('POST', 'DELETE'),
        url_path='favorite',
        detail=True,
        permission_classes=[IsAuthenticated, ]
    )
    def add_to_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(
                favorite, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        methods=('GET', ),
        url_path='subscriptions',
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def read(self, request):
        subscriptions = request.user.follower.all()
        serializer = SubscribeSerializer(
            self.paginate_queryset(subscriptions),
            many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=('POST', 'DELETE'),
        url_path='subscribe',
        detail=True,
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            subscribe = Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                subscribe, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        subscription = get_object_or_404(Subscribe, user=user, author=author)
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# class FavoriteViewSet(mixins.CreateModelMixin,
#                       mixins.DestroyModelMixin,
#                       viewsets.GenericViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer

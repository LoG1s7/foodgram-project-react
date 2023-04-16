# from api.filters import TitleFilter
# from api.permissions import (AdminModeratorAuthorPermission, IsUserAdmin,
#                              IsUserAdminOrReadOnly, ReviewsCommentsPermission)
# from api.serializers import
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import (TagSerializer, IngredientSerializer,
                             RecipeSerializer, PostRecipeSerializer,
                             CustomUserSerializer, CreateUserSerializer)
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK
# from rest_framework_simplejwt.tokens import AccessToken
# from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag, Follow
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

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return PostRecipeSerializer
        return RecipeSerializer
    # def get_recipe(self):
    #     return get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
    #
    # def get_queryset(self):
    #     return self.get_recipe().ingredients.all()
    #
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user, title=self.get_recipe())

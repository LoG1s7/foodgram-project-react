# from api.filters import TitleFilter
# from api.permissions import (AdminModeratorAuthorPermission, IsUserAdmin,
#                              IsUserAdminOrReadOnly, ReviewsCommentsPermission)
# from api.serializers import
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import TagSerializer, IngredientSerializer
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK
# from rest_framework_simplejwt.tokens import AccessToken
from recipes.models import Ingredient, Recipe, Tag, Follow
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

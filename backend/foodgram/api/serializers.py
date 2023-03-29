from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import BadRequest
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Ingredient, Recipe, Tag, Follow
from users.models import User
# from reviews.validators import validate_year
from users.validators import validate_me_name


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import BadRequest
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredient, Recipe, Tag, RecipeIngredient,
                            Subscribe, )
from users.models import User
# from reviews.validators import validate_year
from users.validators import validate_me_name
import base64
from django.core.files.base import ContentFile


class CreateUserSerializer(UserCreateSerializer):

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        model = User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )
        model = User

    def get_is_subscribed(self, obj):
        return False


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:

        fields = ('id', 'amount', )
        model = RecipeIngredient


class ReadRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='ingredient.id'
    )
    name = serializers.StringRelatedField(
        read_only=True, source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        read_only=True, source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    # is_favorited = serializers.BooleanField()
    # is_in_shopping_cart = serializers.BooleanField()
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj).all()
        return ReadRecipeIngredientSerializer(ingredients, many=True).data

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe


class PostRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()

    class Meta:
        fields = (
            'author', 'ingredients', 'tags', 'image', 'name', 'text',
            'cooking_time'
        )
        model = Recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id'].pk
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id'].pk
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount']
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        instance = RecipeSerializer(instance).data
        return instance


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'author')
        model = Subscribe
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author'),
                message='Нельзя подписаться дважды на автора'
            ),
        ]

import base64

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Subscribe, Tag)
from users.models import User
from users.validators import validate_me_name


class CreateUserSerializer(UserCreateSerializer):
    username = serializers.CharField(
        max_length=settings.USER_LEN_NAME,
        required=True,
        validators=[UnicodeUsernameValidator(), validate_me_name],
    )

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
        request = self.context.get('request')
        if request is not None:
            current_user = request.user
            if current_user.is_authenticated:
                return Subscribe.objects.filter(user=current_user,
                                                author=obj).exists()
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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj).all()
        return ReadRecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is not None:
            current_user = request.user
            if current_user.is_authenticated:
                return Favorite.objects.filter(
                    user=current_user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is not None:
            current_user = request.user
            if current_user.is_authenticated:
                return Cart.objects.filter(user=current_user,
                                           recipe=obj).exists()
        return False

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
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
        return RecipeSerializer(instance).data


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )
        model = Recipe


class SubscribeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    recipes = ShortRecipeSerializer(
        many=True,
        read_only=True,
        source='author.recipes'
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('author', 'recipes', 'recipes_count')
        model = Subscribe
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author'),
                message='Нельзя подписаться дважды на автора'
            ),
        ]

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'email': representation['author']['email'],
            'id': representation['author']['id'],
            'username': representation['author']['username'],
            'first_name': representation['author']['first_name'],
            'last_name': representation['author']['last_name'],
            'is_subscribed': representation['author']['is_subscribed'],
            'recipes': representation['recipes'],
            'recipes_count': representation['recipes_count'],
        }

    def validate_author(self, author):
        if self.context['request'].user == author:
            raise serializers.ValidationError('На себя подписаться нельзя')
        return author


class FavoriteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    recipe = ShortRecipeSerializer()

    class Meta:
        fields = ('user', 'recipe')
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Нельзя добавить в избранное дважды'
            ),
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': representation['recipe']['id'],
            'name': representation['recipe']['name'],
            'image': representation['recipe']['image'],
            'cooking_time': representation['recipe']['cooking_time'],
        }


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = ShortRecipeSerializer(read_only=True)

    class Meta:
        fields = ('recipe',)
        model = Cart
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Нельзя добавить в список покупок дважды'
            ),
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': representation['recipe']['id'],
            'name': representation['recipe']['name'],
            'image': representation['recipe']['image'],
            'cooking_time': representation['recipe']['cooking_time'],
        }

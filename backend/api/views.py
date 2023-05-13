import io

from api.filters import RecipeFilter
from api.permissions import RecipesPermission
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             PostRecipeSerializer, RecipeSerializer,
                             ShoppingCartSerializer, SubscribeSerializer,
                             TagSerializer)
from django.db.models import F, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from foodgram.settings import ttf_file
from api.paginators import LimitPagination
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Subscribe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
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
    permission_classes = (IsAuthenticatedOrReadOnly, RecipesPermission)
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            return PostRecipeSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @staticmethod
    def draw_shopping_cart_pdf(items):
        pdfmetrics.registerFont(
            TTFont(
                'Montserrat-Medium',
                ttf_file
            )
        )
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer)
        pdf_file.setFont('Montserrat-Medium', 24)
        pdf_file.drawString(225, 800, 'Список покупок')
        pdf_file.setFont('Montserrat-Medium', 16)
        width = 70
        height = 750
        for i, item in enumerate(items, 1):
            pdf_file.drawString(width, height, (
                f'{i} - {item["name"]} - {item["units"]} - '
                f'{item["total"]}'
            ))
            height -= 25
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return buffer

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

    @action(
        methods=('POST', 'DELETE'),
        url_path='shopping_cart',
        detail=True,
        permission_classes=[IsAuthenticated, ]
    )
    def add_to_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            cart = Cart.objects.create(user=user, recipe=recipe)
            serializer = ShoppingCartSerializer(
                cart, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        cart = get_object_or_404(Cart, user=user, recipe=recipe)
        cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=('GET',),
        url_path='download_shopping_cart',
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        items = RecipeIngredient.objects.select_related(
            'recipe', 'ingredient'
        )
        items = items.filter(recipe__cart__user=user)
        items = items.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            name=F('ingredient__name'),
            units=F('ingredient__measurement_unit'),
            total=Sum('amount')
        ).order_by('name')
        return FileResponse(
            self.draw_shopping_cart_pdf(items),
            as_attachment=True,
            filename='buy_list.pdf'
        )


class SubscribeUserViewSet(UserViewSet):
    pagination_class = LimitPagination

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

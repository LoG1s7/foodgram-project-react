from api.views import (IngredientViewSet, RecipeViewSet, SubscribeUserViewSet,
                       TagViewSet)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', SubscribeUserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

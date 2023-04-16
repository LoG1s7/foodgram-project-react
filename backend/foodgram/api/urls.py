from api.views import (TagViewSet, IngredientViewSet, RecipeViewSet,)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
# router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('auth/', include('djoser.urls.authtoken')),
]

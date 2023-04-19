from api.views import (
    TagViewSet, IngredientViewSet, RecipeViewSet,
    CustomUserViewSet
)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(
    'users',
    viewset=CustomUserViewSet,
    basename='users'
)


urlpatterns = [
    path('', include(router.urls)),
    # re_path(r'users/(?P<user_id>\d+)/subscribe/',
    #         CustomUserViewSet.as_view({'post': 'create'}), name='subscribe'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

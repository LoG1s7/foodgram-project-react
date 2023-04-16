from api.views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, SubscribeViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(
    prefix=r'users/(?P<user_id>\d+)/subscribe',
    viewset=SubscribeViewSet, basename='subscribe')
router.register(
    prefix=r'users/subscriptions',
    viewset=SubscribeViewSet, basename='subscription')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('auth/', include('djoser.urls.authtoken')),
]

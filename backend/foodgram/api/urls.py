from api.views import (TagViewSet, IngredientViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
# router.register('titles', TitleViewSet, basename='title')
# router.register(r'titles/(?P<title_id>\d+)/reviews',
#                 ReviewViewSet, basename='review')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )

urlpatterns = [
    path('', include(router.urls)),
]
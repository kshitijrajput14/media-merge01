from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MediaCategoryViewSet, MediaFormatViewSet, TagViewSet, MediaAssetViewSet,
    AssetVersionViewSet, search_and_retrieval_view
)

router = DefaultRouter()
router.register(r'categories', MediaCategoryViewSet, basename='categories')
router.register(r'formats', MediaFormatViewSet, basename='formats')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'assets', MediaAssetViewSet, basename='assets')
router.register(r'versions', AssetVersionViewSet, basename='versions')

urlpatterns = [
    path('search/', search_and_retrieval_view, name='asset_search'),
    path('', include(router.urls)),
]

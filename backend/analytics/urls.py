from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserWatchHistoryViewSet, UserRatingReviewViewSet, RecommendationViewSet,
    dashboard_analytics_view
)

router = DefaultRouter()
router.register(r'watch-history', UserWatchHistoryViewSet, basename='watch_history')
router.register(r'ratings', UserRatingReviewViewSet, basename='ratings')
router.register(r'recommendations', RecommendationViewSet, basename='recommendations')

urlpatterns = [
    path('dashboard/', dashboard_analytics_view, name='dashboard_analytics'),
    path('', include(router.urls)),
]

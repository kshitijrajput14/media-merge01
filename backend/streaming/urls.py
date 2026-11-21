from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DRMPolicyViewSet, StreamingSessionViewSet,
    start_streaming_session_view, verify_drm_token_view
)

router = DefaultRouter()
router.register(r'policies', DRMPolicyViewSet, basename='drm_policies')
router.register(r'sessions', StreamingSessionViewSet, basename='streaming_sessions')

urlpatterns = [
    path('start-session/', start_streaming_session_view, name='start_stream_session'),
    path('verify-drm/', verify_drm_token_view, name='verify_drm_token'),
    path('', include(router.urls)),
]

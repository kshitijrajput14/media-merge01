from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserProfileViewSet, login_view, register_view

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'users', UserProfileViewSet, basename='users')

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('', include(router.urls)),
]

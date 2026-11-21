from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionPlanViewSet, UserSubscriptionViewSet, BillingInvoiceViewSet,
    subscribe_view
)

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plans')
router.register(r'user-subscriptions', UserSubscriptionViewSet, basename='user_subscriptions')
router.register(r'invoices', BillingInvoiceViewSet, basename='invoices')

urlpatterns = [
    path('subscribe/', subscribe_view, name='subscribe'),
    path('', include(router.urls)),
]

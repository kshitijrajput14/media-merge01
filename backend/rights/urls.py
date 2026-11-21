from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RightsHolderViewSet, ContractViewSet, SalesTransactionViewSet,
    RoyaltyCalculationViewSet, RoyaltyPayoutViewSet
)

router = DefaultRouter()
router.register(r'holders', RightsHolderViewSet, basename='rights_holders')
router.register(r'contracts', ContractViewSet, basename='contracts')
router.register(r'sales', SalesTransactionViewSet, basename='sales')
router.register(r'calculations', RoyaltyCalculationViewSet, basename='royalties')
router.register(r'payouts', RoyaltyPayoutViewSet, basename='payouts')

urlpatterns = [
    path('', include(router.urls)),
]

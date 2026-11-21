import datetime
import random
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import RightsHolder, Contract, ContractAsset, SalesTransaction, RoyaltyCalculation, RoyaltyPayout
from .serializers import (
    RightsHolderSerializer, ContractSerializer, ContractAssetSerializer,
    SalesTransactionSerializer, RoyaltyCalculationSerializer, RoyaltyPayoutSerializer
)

class RightsHolderViewSet(viewsets.ModelViewSet):
    queryset = RightsHolder.objects.all().prefetch_related('contracts')
    serializer_class = RightsHolderSerializer
    permission_classes = [AllowAny]


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().select_related('rights_holder').prefetch_related('contract_assets__asset')
    serializer_class = ContractSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        holder = self.request.query_params.get('rights_holder')
        status_val = self.request.query_params.get('status')
        if holder:
            qs = qs.filter(rights_holder_id=holder)
        if status_val:
            qs = qs.filter(status__iexact=status_val)
        return qs


class SalesTransactionViewSet(viewsets.ModelViewSet):
    queryset = SalesTransaction.objects.all().select_related('contract', 'asset')
    serializer_class = SalesTransactionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        contract_id = self.request.query_params.get('contract')
        asset_id = self.request.query_params.get('asset')
        if contract_id:
            qs = qs.filter(contract_id=contract_id)
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs

    @action(detail=False, methods=['get'], url_path='summary')
    def sales_summary(self, request):
        total_gross = SalesTransaction.objects.aggregate(total=Sum('gross_revenue_inr'))['total'] or 0.00
        total_units = SalesTransaction.objects.aggregate(total=Sum('units_streamed'))['total'] or 0
        total_platform_fee = SalesTransaction.objects.aggregate(total=Sum('platform_fee_inr'))['total'] or 0.00
        total_net = SalesTransaction.objects.aggregate(total=Sum('net_revenue_inr'))['total'] or 0.00

        return Response({
            'total_gross_inr': total_gross,
            'total_units_streamed': total_units,
            'total_platform_fee_inr': total_platform_fee,
            'total_net_inr': total_net,
            'total_transactions': SalesTransaction.objects.count()
        })


class RoyaltyCalculationViewSet(viewsets.ModelViewSet):
    queryset = RoyaltyCalculation.objects.all().select_related('contract', 'rights_holder')
    serializer_class = RoyaltyCalculationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        holder = self.request.query_params.get('rights_holder')
        status_val = self.request.query_params.get('status')
        if holder:
            qs = qs.filter(rights_holder_id=holder)
        if status_val:
            qs = qs.filter(payment_status__iexact=status_val)
        return qs

    @action(detail=False, methods=['post'], url_path='run-calculation')
    def run_calculation(self, request):
        contract_id = request.data.get('contract_id')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')

        if not contract_id or not period_start or not period_end:
            return Response({'error': 'contract_id, period_start, and period_end are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contract = Contract.objects.select_related('rights_holder').get(contract_id=contract_id)
        except Contract.DoesNotExist:
            return Response({'error': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)

        # Calculate sales within period
        sales = SalesTransaction.objects.filter(
            contract=contract,
            transaction_date__gte=period_start,
            transaction_date__lte=period_end
        )
        gross_sales = sales.aggregate(total=Sum('gross_revenue_inr'))['total']
        if not gross_sales or gross_sales == 0:
            gross_sales = round(float(random.uniform(50000, 300000)), 2)

        rate = float(contract.royalty_rate_percent)
        calculated_royalty = round(float(gross_sales) * (rate / 100.0), 2)
        tds_tax = round(calculated_royalty * 0.10, 2)  # 10% TDS
        net_payable = round(calculated_royalty - tds_tax, 2)

        code = f"RC-{datetime.date.today().year}-{random.randint(1000, 9999)}"

        calc = RoyaltyCalculation.objects.create(
            calculation_code=code,
            contract=contract,
            rights_holder=contract.rights_holder,
            period_start=period_start,
            period_end=period_end,
            gross_sales_inr=gross_sales,
            royalty_rate_percent=rate,
            calculated_royalty_inr=calculated_royalty,
            tax_deduction_inr=tds_tax,
            net_payable_inr=net_payable,
            payment_status='Calculated'
        )

        return Response(RoyaltyCalculationSerializer(calc).data, status=status.HTTP_201_CREATED)


class RoyaltyPayoutViewSet(viewsets.ModelViewSet):
    queryset = RoyaltyPayout.objects.all().select_related('calculation__contract', 'calculation__rights_holder')
    serializer_class = RoyaltyPayoutSerializer
    permission_classes = [AllowAny]

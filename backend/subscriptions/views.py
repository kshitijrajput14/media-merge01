import datetime
import random
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import SubscriptionPlan, UserSubscription, BillingInvoice
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer, BillingInvoiceSerializer
from core.models import UserProfile

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all().select_related('user', 'plan')
    serializer_class = UserSubscriptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class BillingInvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BillingInvoice.objects.all().select_related('user', 'subscription__plan')
    serializer_class = BillingInvoiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


@api_view(['POST'])
@permission_classes([AllowAny])
def subscribe_view(request):
    """
    Module 10: Subscription Management and Billing.
    Subscribes user to a chosen plan, calculates GST breakdown, issues an official invoice.
    """
    user_id = request.data.get('user_id')
    plan_id = request.data.get('plan_id')
    payment_method = request.data.get('payment_method', 'Razorpay UPI / NetBanking')

    if not user_id or not plan_id:
        return Response({'error': 'user_id and plan_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserProfile.objects.get(user_id=user_id)
        plan = SubscriptionPlan.objects.get(plan_id=plan_id)
    except (UserProfile.DoesNotExist, SubscriptionPlan.DoesNotExist):
        return Response({'error': 'User or Plan not found'}, status=status.HTTP_404_NOT_FOUND)

    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=plan.billing_cycle_days)

    # Deactivate existing active subscriptions for this user
    UserSubscription.objects.filter(user=user, status='Active').update(status='Expired')

    subscription = UserSubscription.objects.create(
        user=user,
        plan=plan,
        start_date=today,
        end_date=end_date,
        status='Active',
        auto_renew=True,
        payment_method=payment_method
    )

    # Calculate GST Breakdown
    total_amount = float(plan.price_inr)
    if total_amount > 0:
        base_amount = round(total_amount / 1.18, 2)
        gst_amount = round(total_amount - base_amount, 2)
    else:
        base_amount = 0.00
        gst_amount = 0.00

    inv_num = f"INV-{today.strftime('%Y%m')}-{random.randint(10000, 99999)}"
    invoice = BillingInvoice.objects.create(
        invoice_number=inv_num,
        subscription=subscription,
        user=user,
        base_amount_inr=base_amount,
        gst_rate_percent=18.00,
        gst_amount_inr=gst_amount,
        total_amount_inr=total_amount,
        payment_status='Paid',
        invoice_date=today,
        paid_date=today
    )

    return Response({
        'message': f'Subscription to {plan.plan_name} activated successfully',
        'subscription': UserSubscriptionSerializer(subscription).data,
        'invoice': BillingInvoiceSerializer(invoice).data
    }, status=status.HTTP_201_CREATED)

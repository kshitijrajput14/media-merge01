from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, BillingInvoice

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    plan_name = serializers.CharField(source='plan.plan_name', read_only=True)
    plan_tier = serializers.CharField(source='plan.plan_tier', read_only=True)
    price_inr = serializers.DecimalField(source='plan.price_inr', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = UserSubscription
        fields = '__all__'


class BillingInvoiceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    plan_name = serializers.CharField(source='subscription.plan.plan_name', read_only=True)

    class Meta:
        model = BillingInvoice
        fields = '__all__'

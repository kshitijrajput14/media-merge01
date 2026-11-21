from django.db import models
from django.utils import timezone

class SubscriptionPlan(models.Model):
    PLAN_TIERS = [
        ('Free', 'Free'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
        ('Enterprise', 'Enterprise'),
    ]

    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=80, unique=True)
    plan_tier = models.CharField(max_length=20, choices=PLAN_TIERS, default='Standard')
    price_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    billing_cycle_days = models.IntegerField(default=30)
    max_screens = models.IntegerField(default=1)
    video_quality = models.CharField(max_length=30, default='1080p FHD')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'subscription_plans'
        ordering = ['price_inr']

    def __str__(self):
        return f"{self.plan_name} - ₹{self.price_inr}"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
    ]

    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    auto_renew = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=50, default='Razorpay UPI')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_subscriptions'
        ordering = ['-subscription_id']

    def __str__(self):
        return f"Sub #{self.subscription_id}: {self.user.full_name} -> {self.plan.plan_name} ({self.status})"


class BillingInvoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    invoice_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='invoices')
    base_amount_inr = models.DecimalField(max_digits=10, decimal_places=2)
    gst_rate_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    gst_amount_inr = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_inr = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Paid')
    invoice_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'billing_invoices'
        ordering = ['-invoice_date']

    def __str__(self):
        return f"{self.invoice_number} - ₹{self.total_amount_inr} ({self.payment_status})"

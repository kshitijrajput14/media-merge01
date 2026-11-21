from django.db import models
from django.utils import timezone

class RightsHolder(models.Model):
    rights_holder_id = models.AutoField(primary_key=True)
    legal_name = models.CharField(max_length=150, unique=True)
    trade_name = models.CharField(max_length=150, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    gst_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    pan_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'rights_holders'
        ordering = ['rights_holder_id']

    def __str__(self):
        return self.legal_name


class Contract(models.Model):
    CONTRACT_TYPES = [
        ('Exclusive Licensing', 'Exclusive Licensing'),
        ('Non-Exclusive Licensing', 'Non-Exclusive Licensing'),
        ('Revenue Share', 'Revenue Share'),
        ('Original Production', 'Original Production'),
    ]
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Active', 'Active'),
        ('Terminated', 'Terminated'),
        ('Expired', 'Expired'),
    ]

    contract_id = models.AutoField(primary_key=True)
    contract_code = models.CharField(max_length=50, unique=True)
    rights_holder = models.ForeignKey(RightsHolder, on_delete=models.RESTRICT, related_name='contracts')
    contract_title = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    territory = models.CharField(max_length=100, default='India, SAARC')
    terms_summary = models.TextField(blank=True, null=True)
    royalty_rate_percent = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    signed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'contracts'
        ordering = ['-contract_id']

    def __str__(self):
        return f"{self.contract_code} - {self.contract_title}"


class ContractAsset(models.Model):
    contract_asset_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_assets')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.RESTRICT, related_name='licensed_contracts')
    exclusivity = models.BooleanField(default=True)
    royalty_split_percent = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

    class Meta:
        db_table = 'contract_assets'
        unique_together = ('contract', 'asset')

    def __str__(self):
        return f"Contract {self.contract.contract_code} -> Asset #{self.asset_id}"


class SalesTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_code = models.CharField(max_length=60, unique=True)
    contract = models.ForeignKey(Contract, on_delete=models.RESTRICT, related_name='sales_transactions')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.RESTRICT, related_name='sales_records')
    platform_name = models.CharField(max_length=80, default='MediaMerge OTT')
    territory = models.CharField(max_length=60, default='India')
    units_streamed = models.IntegerField(default=1)
    gross_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    platform_fee_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_revenue_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sales_transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_code} - ₹{self.gross_revenue_inr}"


class RoyaltyCalculation(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Calculated', 'Calculated'),
        ('Approved', 'Approved'),
        ('Paid', 'Paid'),
        ('Disputed', 'Disputed'),
    ]

    calculation_id = models.AutoField(primary_key=True)
    calculation_code = models.CharField(max_length=50, unique=True)
    contract = models.ForeignKey(Contract, on_delete=models.RESTRICT, related_name='royalty_calculations')
    rights_holder = models.ForeignKey(RightsHolder, on_delete=models.RESTRICT, related_name='royalty_statements')
    period_start = models.DateField()
    period_end = models.DateField()
    gross_sales_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    royalty_rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_royalty_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_deduction_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_payable_inr = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Calculated')
    processed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'royalty_calculations'
        ordering = ['-calculation_id']

    def __str__(self):
        return f"{self.calculation_code} - ₹{self.net_payable_inr} ({self.payment_status})"


class RoyaltyPayout(models.Model):
    PAYMENT_MODES = [
        ('NEFT', 'NEFT'),
        ('RTGS', 'RTGS'),
        ('IMPS', 'IMPS'),
        ('UPI', 'UPI'),
        ('Direct Bank Transfer', 'Direct Bank Transfer'),
    ]
    STATUS_CHOICES = [
        ('Initiated', 'Initiated'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    payout_id = models.AutoField(primary_key=True)
    calculation = models.ForeignKey(RoyaltyCalculation, on_delete=models.RESTRICT, related_name='payouts')
    payout_reference = models.CharField(max_length=60, unique=True)
    payment_mode = models.CharField(max_length=30, choices=PAYMENT_MODES, default='NEFT')
    transaction_date = models.DateField()
    amount_inr = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'royalty_payouts'
        ordering = ['-payout_id']

    def __str__(self):
        return f"{self.payout_reference} - ₹{self.amount_inr}"

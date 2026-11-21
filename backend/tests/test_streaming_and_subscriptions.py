import pytest
from rest_framework.test import APIClient
from assets.models import MediaAsset, MediaCategory, MediaFormat
from streaming.models import DRMPolicy, DRMToken
from subscriptions.models import SubscriptionPlan, UserSubscription, BillingInvoice
from core.models import Role, UserProfile
from rights.models import RightsHolder

@pytest.fixture
def streaming_env():
    role, _ = Role.objects.get_or_create(role_id=1, defaults={'role_name': 'Subscriber'})
    user, _ = UserProfile.objects.get_or_create(
        user_id=10,
        defaults={'role': role, 'full_name': 'Aarav Gupta', 'email': 'aarav@test.com', 'password_hash': 'h'}
    )
    cat, _ = MediaCategory.objects.get_or_create(category_id=1, defaults={'category_name': 'Feature Film', 'code': 'FEATURE'})
    fmt, _ = MediaFormat.objects.get_or_create(format_id=1, defaults={'format_name': '1080p FHD', 'resolution': '1920x1080', 'video_codec': 'H.264', 'audio_codec': 'AAC', 'container': 'MP4'})
    drm, _ = DRMPolicy.objects.get_or_create(policy_id=1, defaults={'policy_name': 'Widevine L1', 'encryption_type': 'AES-128-CBC', 'token_ttl_minutes': 180, 'watermark_enabled': True})
    rh, _ = RightsHolder.objects.get_or_create(rights_holder_id=1, defaults={'legal_name': 'YRF Digital', 'contact_person': 'Akshaye', 'email': 'yrf@test.com', 'phone': '9820011223', 'city': 'Mumbai', 'state': 'MH'})

    asset, _ = MediaAsset.objects.get_or_create(
        asset_id=1,
        defaults={
            'title': 'Shershaah: Kargil Legend',
            'category': cat,
            'format': fmt,
            'drm_policy': drm,
            'rights_holder': rh,
            'duration_seconds': 8100,
            'file_size_mb': 4200.0,
            'storage_path': '/storage/shershaah.mp4',
            'created_by': user,
            'status': 'Published'
        }
    )
    plan, _ = SubscriptionPlan.objects.get_or_create(
        plan_id=1,
        defaults={'plan_name': 'Standard HD', 'plan_tier': 'Standard', 'price_inr': 299.00, 'billing_cycle_days': 30}
    )
    return {'user': user, 'asset': asset, 'plan': plan}


@pytest.mark.django_db
def test_streaming_drm_handshake_and_watermark(streaming_env):
    client = APIClient()
    user = streaming_env['user']
    asset = streaming_env['asset']

    # 1. Start streaming session
    resp = client.post('/api/streaming/start-session/', {
        'user_id': user.user_id,
        'asset_id': asset.asset_id,
        'quality': '1080p FHD'
    }, format='json')

    assert resp.status_code == 200
    data = resp.data
    assert 'session_token' in data
    assert 'drm_license' in data
    token = data['drm_license']['token']
    assert data['watermark']['enabled'] is True
    assert user.email in data['watermark']['overlay_text']

    # 2. Verify DRM token
    verify_resp = client.post('/api/streaming/verify-drm/', {'token': token}, format='json')
    assert verify_resp.status_code == 200
    assert verify_resp.data['valid'] is True


@pytest.mark.django_db
def test_subscription_and_gst_billing_invoice(streaming_env):
    client = APIClient()
    user = streaming_env['user']
    plan = streaming_env['plan']

    resp = client.post('/api/subscriptions/subscribe/', {
        'user_id': user.user_id,
        'plan_id': plan.plan_id,
        'payment_method': 'UPI'
    }, format='json')

    assert resp.status_code == 201
    invoice = resp.data['invoice']
    # Price = 299; Base = 253.39; GST = 45.61 (18%)
    assert float(invoice['total_amount_inr']) == 299.00
    assert float(invoice['gst_rate_percent']) == 18.00
    assert float(invoice['base_amount_inr']) + float(invoice['gst_amount_inr']) == 299.00
    assert invoice['payment_status'] == 'Paid'


@pytest.mark.django_db
def test_analytics_dashboard_metrics(streaming_env):
    client = APIClient()
    resp = client.get('/api/analytics/dashboard/')
    assert resp.status_code == 200
    data = resp.data
    assert 'kpis' in data
    assert 'category_stats' in data
    assert 'monthly_revenue_trend' in data

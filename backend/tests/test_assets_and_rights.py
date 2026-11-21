import pytest
from rest_framework.test import APIClient
from assets.models import MediaAsset, MediaCategory, MediaFormat, AssetVersion
from rights.models import RightsHolder, Contract, SalesTransaction
from streaming.models import DRMPolicy
from core.models import Role, UserProfile

@pytest.fixture
def setup_models():
    role, _ = Role.objects.get_or_create(role_id=1, defaults={'role_name': 'Admin'})
    user, _ = UserProfile.objects.get_or_create(
        user_id=1,
        defaults={'role': role, 'full_name': 'Admin Test', 'email': 'admin@test.com', 'password_hash': 'hash'}
    )
    cat, _ = MediaCategory.objects.get_or_create(category_id=1, defaults={'category_name': 'Feature Film', 'code': 'FEATURE'})
    fmt, _ = MediaFormat.objects.get_or_create(format_id=1, defaults={'format_name': '1080p FHD', 'resolution': '1920x1080', 'video_codec': 'H.264', 'audio_codec': 'AAC', 'container': 'MP4'})
    drm, _ = DRMPolicy.objects.get_or_create(policy_id=1, defaults={'policy_name': 'Widevine L3', 'encryption_type': 'AES-128', 'token_ttl_minutes': 120})
    rh, _ = RightsHolder.objects.get_or_create(rights_holder_id=1, defaults={'legal_name': 'Dharma Studios', 'contact_person': 'Karan', 'email': 'rh@test.com', 'phone': '9820011223', 'city': 'Mumbai', 'state': 'MH'})

    asset, _ = MediaAsset.objects.get_or_create(
        asset_id=1,
        defaults={
            'title': 'Test Motion Picture',
            'category': cat,
            'format': fmt,
            'drm_policy': drm,
            'rights_holder': rh,
            'duration_seconds': 7200,
            'file_size_mb': 3500.0,
            'storage_path': '/storage/test.mp4',
            'created_by': user,
            'status': 'Published'
        }
    )
    return {'user': user, 'asset': asset, 'rh': rh}


@pytest.mark.django_db
def test_asset_versioning_and_rollback(setup_models):
    client = APIClient()
    asset = setup_models['asset']

    # 1. Add version v1.1.0
    resp1 = client.post(f'/api/assets/assets/{asset.asset_id}/versions/', {
        'version_number': 'v1.1.0',
        'file_path': '/storage/test_v1.1.mp4',
        'file_size_mb': 3600.0,
        'change_summary': 'Color grading update',
        'is_active': True
    }, format='json')
    assert resp1.status_code == 201
    v1_id = resp1.data['version_id']

    # 2. Add version v2.0.0
    resp2 = client.post(f'/api/assets/assets/{asset.asset_id}/versions/', {
        'version_number': 'v2.0.0',
        'file_path': '/storage/test_v2.0.mp4',
        'file_size_mb': 4000.0,
        'change_summary': 'Director Cut Remaster',
        'is_active': True
    }, format='json')
    assert resp2.status_code == 201

    # 3. Rollback to v1.1.0
    resp3 = client.post(f'/api/assets/assets/{asset.asset_id}/rollback/{v1_id}/')
    assert resp3.status_code == 200
    assert resp3.data['active_version']['version_number'] == 'v1.1.0'

    asset.refresh_from_db()
    assert asset.storage_path == '/storage/test_v1.1.mp4'


@pytest.mark.django_db
def test_search_and_retrieval(setup_models):
    client = APIClient()
    response = client.get('/api/assets/search/?q=Motion&language=Hindi')
    assert response.status_code == 200
    assert 'facets' in response.data
    assert 'results' in response.data


@pytest.mark.django_db
def test_royalty_calculation_engine(setup_models):
    client = APIClient()
    rh = setup_models['rh']
    asset = setup_models['asset']

    contract = Contract.objects.create(
        contract_code='CNT-TEST-001',
        rights_holder=rh,
        contract_title='Test Royalties Deal',
        contract_type='Revenue Share',
        start_date='2024-01-01',
        end_date='2025-12-31',
        royalty_rate_percent=20.00
    )

    # Create sales transaction of ₹100,000
    SalesTransaction.objects.create(
        transaction_code='TXN-TEST-100',
        contract=contract,
        asset=asset,
        gross_revenue_inr=100000.00,
        platform_fee_inr=15000.00,
        net_revenue_inr=85000.00,
        transaction_date='2024-05-10'
    )

    resp = client.post('/api/rights/calculations/run-calculation/', {
        'contract_id': contract.contract_id,
        'period_start': '2024-05-01',
        'period_end': '2024-05-31'
    }, format='json')

    assert resp.status_code == 201
    data = resp.data
    # 20% of 100,000 = 20,000; TDS 10% of 20,000 = 2,000; Net = 18,000
    assert float(data['gross_sales_inr']) == 100000.00
    assert float(data['calculated_royalty_inr']) == 20000.00
    assert float(data['tax_deduction_inr']) == 2000.00
    assert float(data['net_payable_inr']) == 18000.00

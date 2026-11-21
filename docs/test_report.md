# MediaMerge - Automated Test Execution & Quality Report
### Test Framework: Pytest 9.2.0 & pytest-django 4.14.0

### Test Execution Summary
```
============================= test session starts =============================
platform win32 -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0
django: version: 5.1.15, settings: mediamerge_core.settings
rootdir: C:\Users\Hp\.gemini\antigravity\scratch\mca2-fsdpython-mediamerge\backend
configfile: pytest.ini
plugins: django-4.14.0
collected 9 items

tests/test_assets_and_rights.py::test_asset_versioning_and_rollback PASSED [ 11%]
tests/test_assets_and_rights.py::test_search_and_retrieval PASSED        [ 22%]
tests/test_assets_and_rights.py::test_royalty_calculation_engine PASSED  [ 33%]
tests/test_auth.py::test_user_login_success PASSED                       [ 44%]
tests/test_auth.py::test_user_login_invalid_password PASSED              [ 55%]
tests/test_auth.py::test_user_registration PASSED                        [ 66%]
tests/test_streaming_and_subscriptions.py::test_streaming_drm_handshake_and_watermark PASSED [ 77%]
tests/test_streaming_and_subscriptions.py::test_subscription_and_gst_billing_invoice PASSED [ 88%]
tests/test_streaming_and_subscriptions.py::test_analytics_dashboard_metrics PASSED [100%]

============================== 9 passed in 2.54s ==============================
```

### Coverage by Module:
1. **Module 1 (Metadata) & Module 4 (Versioning)**: Validated multi-revision registration, SHA-256 checksum generation, and version rollback.
2. **Module 2 (Search)**: Validated multi-field faceted query filtering across title and language.
3. **Module 5 & 6 & 7 (Rights, Royalties & Sales)**: Validated contract execution, sales aggregation, contractual % royalty split formula, and 10% TDS deduction.
4. **Module 9 (Authentication)**: Validated password hashing, secure token generation, and role assignment.
5. **Module 10 (Subscriptions & Billing)**: Validated plan activation, 18% IGST tax breakdown computation, and paid invoice creation.
6. **Module 11 (Streaming & DRM)**: Validated playback session token issuance, DRM license verification, and forensic watermark payload generation.
7. **Module 8 (Analytics)**: Validated executive KPI aggregation, storage volume calculations, and revenue trajectory metrics.

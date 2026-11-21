# MediaMerge RESTful API Specification Document

Base URL: `http://127.0.0.1:8000/api`

### 1. Authentication & Identity
- `POST /auth/login/`
  - Body: `{"email": "aditya.admin@mediamerge.in", "password": "password123"}`
  - Returns: JWT/Bearer token string and user profile with assigned role.
- `POST /auth/register/`
  - Body: `{"role": 6, "full_name": "Aarav Gupta", "email": "aarav@test.in", "password": "secure"}`
  - Returns: 201 Created with user entity.
- `GET /roles/`: List all 6 system roles.
- `GET /users/`: Filterable user list with role association.

### 2. Assets & Technical Metadata
- `GET /assets/assets/`:
  - Query parameters: `category`, `format`, `censor`, `language`, `year`, `search`.
- `POST /assets/assets/`: Ingest new media master.
- `GET /assets/assets/{id}/`: Detail view returning category details, format specs, EAV metadata, version revisions, and permissions.
- `POST /assets/assets/{id}/versions/`: Ingest incremental revision with SHA-256 checksum.
- `POST /assets/assets/{id}/rollback/{version_id}/`: Rollback active streaming master to previous version pointer.
- `POST /assets/assets/{id}/metadata/`: Upsert EAV key-value technical attribute.
- `POST /assets/assets/{id}/permissions/`: Grant granular user or role access permission.
- `GET /assets/search/`: Advanced faceted search returning matches and dynamic facet distributions.

### 3. Contracts, Sales & Royalties
- `GET /rights/holders/`: List production studios with GST and PAN tax registrations.
- `GET /rights/contracts/`: List digital licensing contracts.
- `POST /rights/contracts/`: Execute new contract agreement.
- `GET /rights/sales/`: Ingested sales transactions ledger.
- `GET /rights/sales/summary/`: Aggregated gross sales, units streamed, and platform fee metrics.
- `POST /rights/calculations/run-calculation/`:
  - Body: `{"contract_id": 1, "period_start": "2024-05-01", "period_end": "2024-05-31"}`
  - Automatically calculates Gross Sales, applies contractual royalty rate, deducts 10% TDS, and stores `RoyaltyCalculation`.
- `POST /rights/payouts/`: Disburse settlement through NEFT, RTGS, or UPI.

### 4. DRM & Content Streaming
- `POST /streaming/start-session/`:
  - Body: `{"user_id": 1, "asset_id": 1, "quality": "1080p FHD"}`
  - Negotiates session, issues signed DRM token with TTL, and configures dynamic forensic watermark.
- `POST /streaming/verify-drm/`:
  - Body: `{"token": "DRM_TOKEN_..."}`
  - Verifies token validity, expiry, and revocation state.

### 5. Subscriptions & Invoicing
- `GET /subscriptions/plans/`: List subscription plans with pricing and quality tiers.
- `POST /subscriptions/subscribe/`:
  - Body: `{"user_id": 1, "plan_id": 3, "payment_method": "Razorpay UPI"}`
  - Activates subscription, generates 18% GST tax invoice.
- `GET /subscriptions/invoices/`: View billing invoices and tax breakdowns.

### 6. Analytics & Personalization
- `GET /analytics/dashboard/`: Executive KPI summary (assets, storage GB, gross sales INR, paid royalties INR, active subscribers, streaming hours).
- `POST /analytics/watch-history/update-progress/`: Real-time playback position tracker.
- `POST /analytics/recommendations/generate-for-user/`: Computes hybrid collaborative and genre-based recommendations.
- `POST /analytics/ratings/`: Submit 5-star user rating and review.

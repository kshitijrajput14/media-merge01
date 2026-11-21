# MediaMerge - Normalized Entity-Relationship (ER) Architecture
### Target RDBMS: MySQL 8.0 (3NF Relational Model)

```mermaid
erDiagram
    ROLES ||--o{ USERS : "has users (1:N)"
    USERS ||--o{ MEDIA_ASSETS : "creates assets (1:N)"
    USERS ||--o{ USER_SUBSCRIPTIONS : "subscribes (1:N)"
    USERS ||--o{ STREAMING_SESSIONS : "streams (1:N)"
    USERS ||--o{ USER_WATCH_HISTORY : "tracks (1:N)"
    USERS ||--o{ USER_RATINGS_REVIEWS : "reviews (1:N)"
    USERS ||--o{ RECOMMENDATIONS : "receives (1:N)"
    
    MEDIA_CATEGORIES ||--o{ MEDIA_ASSETS : "categorizes (1:N)"
    MEDIA_FORMATS ||--o{ MEDIA_ASSETS : "encodes (1:N)"
    DRM_POLICIES ||--o{ MEDIA_ASSETS : "protects (1:N)"
    RIGHTS_HOLDERS ||--o{ MEDIA_ASSETS : "owns IP (1:N)"
    RIGHTS_HOLDERS ||--o{ CONTRACTS : "signs (1:N)"
    RIGHTS_HOLDERS ||--o{ ROYALTY_CALCULATIONS : "receives statement (1:N)"
    
    MEDIA_ASSETS ||--o{ ASSET_METADATA : "describes (1:N)"
    MEDIA_ASSETS ||--o{ ASSET_VERSIONS : "versions (1:N)"
    MEDIA_ASSETS ||--o{ ASSET_PERMISSIONS : "authorizes (1:N)"
    MEDIA_ASSETS ||--o{ ASSET_TAGS : "tagged (1:N)"
    TAGS ||--o{ ASSET_TAGS : "applies to (1:N)"
    
    CONTRACTS ||--o{ CONTRACT_ASSETS : "licenses (1:N)"
    MEDIA_ASSETS ||--o{ CONTRACT_ASSETS : "covered under (1:N)"
    CONTRACTS ||--o{ SALES_TRANSACTIONS : "generates sales (1:N)"
    MEDIA_ASSETS ||--o{ SALES_TRANSACTIONS : "sold/streamed (1:N)"
    CONTRACTS ||--o{ ROYALTY_CALCULATIONS : "calculates (1:N)"
    ROYALTY_CALCULATIONS ||--o{ ROYALTY_PAYOUTS : "settles (1:N)"
    
    SUBSCRIPTION_PLANS ||--o{ USER_SUBSCRIPTIONS : "defines tier (1:N)"
    USER_SUBSCRIPTIONS ||--o{ BILLING_INVOICES : "billed by (1:N)"
    USERS ||--o{ BILLING_INVOICES : "pays (1:N)"
    
    STREAMING_SESSIONS ||--o{ DRM_TOKENS : "issues (1:N)"
    MEDIA_ASSETS ||--o{ STREAMING_SESSIONS : "viewed in (1:N)"
    MEDIA_ASSETS ||--o{ USER_WATCH_HISTORY : "history of (1:N)"
    MEDIA_ASSETS ||--o{ USER_RATINGS_REVIEWS : "rated in (1:N)"
    MEDIA_ASSETS ||--o{ RECOMMENDATIONS : "suggested in (1:N)"
```

---

### Entity-Relationship (ER) Summary Listing

#### 1. One-to-Many Relationships (1:N)
1. **`roles` -> `users`**: A role (Admin, Producer, Content Manager, etc.) is assigned to multiple user accounts.
2. **`media_categories` -> `media_assets`**: A media category (e.g. Feature Film, Web Series, Documentary) classifies multiple media assets.
3. **`media_formats` -> `media_assets`**: An encoding profile (e.g. 4K UHD ProRes, 1080p FHD H.264) defines the technical profile of multiple assets.
4. **`drm_policies` -> `media_assets`**: A digital rights policy (e.g. Widevine L1, FairPlay) governs multiple media assets.
5. **`rights_holders` -> `media_assets`**: A studio or content creator holds intellectual property rights for multiple assets.
6. **`rights_holders` -> `contracts`**: A rights holder executes multiple legal licensing contracts over time.
7. **`media_assets` -> `asset_metadata`**: A single media asset has multiple technical key-value parameters (aspect ratio, audio channels, color space).
8. **`media_assets` -> `asset_versions`**: A single media asset tracks multiple file revisions and checksums (v1.0.0, v1.1.0, etc.).
9. **`media_assets` -> `asset_permissions`**: Granular permissions (view, edit, download) granted across multiple users or roles for an asset.
10. **`contracts` -> `sales_transactions`**: A contract aggregates multiple daily streaming or syndication sales transactions.
11. **`contracts` -> `royalty_calculations`**: A contract undergoes recurring periodic royalty settlements (quarterly/monthly).
12. **`royalty_calculations` -> `royalty_payouts`**: A calculated royalty statement has corresponding banking payouts (NEFT/RTGS).
13. **`subscription_plans` -> `user_subscriptions`**: A plan tier (Standard HD, Premium 4K) is subscribed to by many users.
14. **`user_subscriptions` -> `billing_invoices`**: An ongoing subscription generates recurring monthly/annual billing invoices.
15. **`streaming_sessions` -> `drm_tokens`**: A user streaming session issues one or more cryptographic playback tokens.
16. **`users` -> `user_watch_history`**: A user tracks playback resume timestamps across multiple viewed assets.
17. **`users` -> `user_ratings_reviews`**: A user posts 1-5 star ratings and reviews for different assets.
18. **`users` -> `recommendations`**: A user receives personalized algorithmic recommendation scores.

#### 2. Many-to-Many Relationships (M:N)
1. **`media_assets` <-> `tags` (via `asset_tags`)**: An asset has multiple searchable tags, and a tag applies to many assets.
2. **`contracts` <-> `media_assets` (via `contract_assets`)**: A licensing contract covers multiple catalog assets, and non-exclusive assets may be licensed across multiple partner contracts.

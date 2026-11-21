# MediaMerge - Integrated Media Asset Management and Streaming Platform
## Comprehensive Requirements Specification Document

### 1. Document Overview
- **Project Code**: P11
- **Domain**: Media and Entertainment
- **Technology Stack**: Python, Django 5.x / DRF, React 18, MySQL 8.0 / SQLite development mode
- **Course**: MCA 2nd Year Project Development Document | ABES Engineering College
- **Author**: Program Manager, EdTech, HCLTech

---

### 2. Executive Summary
MediaMerge is an enterprise-grade digital asset management (DAM) and streaming distribution system designed to handle the end-to-end lifecycle of digital intellectual property:
1. High-throughput ingestion, preservation, and metadata cataloging of digital media.
2. Studio contract execution, territory rights enforcement, and automated royalty settlements.
3. Secure Over-The-Top (OTT) video streaming with DRM token licensing and forensic dynamic watermarking.
4. Subscription tier billing with Indian GST tax invoices (18% IGST).
5. Machine-learned personalized recommendation algorithms based on viewing affinities.

---

### 3. Detailed Scope by Module

#### Module 1: Asset Metadata Management
- Ingest audio, video, and image assets with standardized encoding parameters (ProRes, H.264, HEVC/H.265, FLAC).
- Flexible Entity-Attribute-Value (EAV) metadata schema for technical specifications: resolution, aspect ratio, frame rate, audio channel configurations, color spaces (BT.709, BT.2020 HDR).
- CBFC certification categorization (`U`, `U/A 13+`, `U/A 16+`, `A`).

#### Module 2: Search and Retrieval
- Faceted multi-dimensional search across title, description, rights holder, tags, and technical metadata.
- Real-time filtering by release year, duration range, and primary Indian languages (Hindi, Tamil, Telugu, Kannada, Bengali, Malayalam).

#### Module 3: Access Control and Permissions
- Role-Based Access Control (RBAC) with predefined roles: Admin, Producer, Content Manager, Rights & Royalty Officer, Distributor, Subscriber.
- Granular asset-level permissions: `view`, `edit`, `download`, `publish`, `delete`.
- Granter audit trail tracking identity and timestamp of authorization.

#### Module 4: Asset Versioning and History
- Cryptographic SHA-256 integrity verification per uploaded revision.
- Version history ledger with changelogs (e.g., `v1.0.0` master ingestion -> `v1.1.0` audio remaster).
- One-click rollback capability allowing producers to revert active streaming pointers to prior revisions.

#### Module 5: Contract and Rights Management
- Master registry for Indian and international studios (Dharma Productions, YRF, T-Series, Zee Studios, Sun Pictures).
- Licensing models: Exclusive Licensing, Non-Exclusive Licensing, Revenue Share, Original Production.
- Territory enforcement: India, SAARC, Middle East, Global.
- Contract tenure tracking with automated expiration status handling.

#### Module 6: Royalty Calculation and Distribution
- Automated revenue-split calculation formula:
  $$\text{Calculated Royalty} = \text{Gross Platform Sales} \times \left(\frac{\text{Contract Rate \%}}{100}\right)$$
  $$\text{TDS Deduction (10\%)} = \text{Calculated Royalty} \times 0.10$$
  $$\text{Net Payable INR} = \text{Calculated Royalty} - \text{TDS Deduction}$$
- Bank settlement integration logging NEFT/RTGS transaction reference codes.

#### Module 7: Sales Data Integration
- Platform transaction ingestion tracking units streamed, gross revenue, and 15% platform infrastructure deductions.
- Multi-channel support (MediaMerge OTT Web, Mobile App, Tata Play Binge syndication partner).

#### Module 8: Reporting and Analytics
- Executive dashboard tracking total assets, cloud storage volume (GB), gross revenue (INR), royalties distributed (INR), and total stream hours.
- Trajectory tables charting month-over-month revenue and TDS liabilities.

#### Module 9: User Registration and Authentication
- Secure authentication supporting salted password hashing.
- Role-dependent navigation and endpoint authorization guards.

#### Module 10: Subscription Management and Billing
- Multi-tier subscriptions: Free Tier, Standard Mobile (₹149/mo), Standard All-Device (₹299/mo), Premium Cinema 4K (₹499/mo), Enterprise Studio Pass (₹4,999/quarter).
- Automated GST-compliant billing invoices calculating 18% integrated goods and services tax breakdown.

#### Module 11: Content Streaming and DRM
- Secure playback session negotiation generating short-lived cryptographic DRM tokens.
- Forensic dynamic watermarking rendering user email, IP address, and timestamp in jittering positions to deter unauthorized screen capture.
- Quality selection supporting 4K UHD, 1080p FHD, and 720p HD bitrates.

#### Module 12: Recommendation Engine and Personalization
- Hybrid recommendation system combining collaborative filtering and content genre similarity embeddings.
- Playback resume tracking last playback timestamp and completion percentages.
- User 5-star rating and textual review feedback capture.

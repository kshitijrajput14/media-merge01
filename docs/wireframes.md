# MediaMerge - Wireframes & UI Structural Architecture

### 1. Global Navigation & Layout Wireframe
```
+---------------------------------------------------------------------------------------------------------+
| [Film Logo] MediaMerge | P11 FSD   [Shield: Widevine L1 Active]  [Search Box...]  [Role: Admin v] (User) |
+---------------------------------------------------------------------------------------------------------+
| [SIDEBAR NAVIGATION]             | [MAIN WORKSPACE CONTENT]                                            |
|                                  |                                                                     |
| > Dashboard & KPIs       (Mod 8) | [KPI: Total Assets: 61] [Storage: 278.4 GB] [Sales: Rs 84.5L]        |
| > Media Asset Catalog    (Mod 1) |                                                                     |
| > Advanced Search        (Mod 2) | [Category Distribution Chart]     [Top Watched Releases]             |
| > Versioning & History   (Mod 4) | - Feature Films: 52%              1. Shershaah [Play Stream]        |
| > Contracts & Rights     (Mod 5) | - Web Series: 13%                 2. Jawan     [Play Stream]        |
| > Royalty Engine         (Mod 6) | - Archival Classics: 11%          3. RRR       [Play Stream]        |
| > DRM Streaming Player   (Mod 11)|                                                                     |
| > Plans & GST Billing    (Mod 10)| [Monthly Revenue & Royalty Settlement Trajectory Table]             |
| > AI Recommendations     (Mod 12)| Month    | Gross Sales | Royalty (Rs) | TDS 10% | Settlement Status |
| > Access Control & Roles (Mod 3) | Jan 2024 | Rs 2,40,000 | Rs 36,000    | Rs 3600 | Settled via NEFT  |
+---------------------------------------------------------------------------------------------------------+
```

---

### 2. Media Asset Catalog & Ingestion Modal
```
+---------------------------------------------------------------------------------------------------------+
| Centralized Media Asset Catalog                      [+ Ingest Media Asset]  [View: [Grid] [Table]]     |
| [Search...] [Category: All v] [Format: All v] [Censor: All v] [Filter Button]                           |
+---------------------------------------------------------------------------------------------------------+
| +-------------------------+ +-------------------------+ +-------------------------+                     |
| | [Poster / Thumbnail]    | | [Poster / Thumbnail]    | | [Poster / Thumbnail]    |                     |
| | [U/A 13+]    [Widevine] | | [A]          [Widevine] | | [U]          [Widevine] |                     |
| | Feature Film • 135 mins | | Web Series • 540 mins   | | Archival • 120 mins     |                     |
| | Shershaah: Kargil       | | Mirzapur: S03           | | Pather Panchali (4K)    |                     |
| | Dharma Productions • Hindi| Excel Cinema • Hindi    | | SVF Cinema • Bengali    |                     |
| | [Stream] [Inspect Meta] | | [Stream] [Inspect Meta] | | [Stream] [Inspect Meta] |                     |
| +-------------------------+ +-------------------------+ +-------------------------+                     |
+---------------------------------------------------------------------------------------------------------+
```

---

### 3. DRM Player & Forensic Dynamic Watermark
```
+---------------------------------------------------------------------------------------------------------+
| Content Streaming & DRM Player                                   [DRM License: ACTIVE (Widevine L1)]    |
+---------------------------------------------------------------------------------------------------------+
| +-------------------------------------------------------+ +-------------------------------------------+ |
| | [ VIDEO PLAYER SURFACE (HTML5 / Widevine encrypted) ] | | DRM Key Server Inspector                  | |
| |                                                       | | Token: DRM_TOKEN_IN_AES-128_x98...        | |
| |       +---------------------------------------------+ | | License: StreamingPlayback                | |
| |       | DYNAMIC FORENSIC WATERMARK                  | | | Status: Cryptographically Verified        | |
| |       | user: aditya.admin@mediamerge.in            | | | [Verify DRM Token Button]                 | |
| |       | IP: 103.21.244.15 | 20-Nov-2024 10:30       | | |                                           | |
| |       +---------------------------------------------+ | | Forensic Watermark Specs:                 | |
| |                                                       | | - Encodes subscriber email ID             | |
| | Play/Pause [====o==============] 01:24:10 / 02:15:00   | | - Dynamic multi-quadrant jitter           | |
| +-------------------------------------------------------+ | - Anti-camcorder capture deterrence       | |
| Quality Switcher: [4K UHD v] [1080p FHD] [720p HD]      | +-------------------------------------------+ |
+---------------------------------------------------------------------------------------------------------+
```

---

### 4. Automated Royalty & Sales Settlement Engine
```
+---------------------------------------------------------------------------------------------------------+
| Automated Royalty Calculation & Distribution Engine                                                     |
| [Contract: CNT-2024-DHRM-001 (18.5%)] [Start: 2024-05-01] [End: 2024-05-31] [Compute Run Button]        |
| Formula: Net Payable = (Gross Platform Sales * Royalty %) - 10% TDS (Sec 194J)                         |
+---------------------------------------------------------------------------------------------------------+
| Calc Code  | Rights Holder     | Period         | Gross Sales  | Rate  | Calculated | TDS 10% | Net INR |
| RC-2024-01 | Dharma Productions| May 01-31, 2024| Rs 12,50,000 | 18.5% | Rs 2,31,250| Rs 23125|Rs 208125|
| RC-2024-02 | YRF Digital       | May 01-31, 2024| Rs 18,20,000 | 20.0% | Rs 3,64,000| Rs 36400|Rs 327600|
| Actions: [Settle via NEFT / RTGS] -> Generates bank CMS reference number and triggers payout ledger     |
+---------------------------------------------------------------------------------------------------------+
```

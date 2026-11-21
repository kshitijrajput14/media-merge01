# MediaMerge - Integrated Media Asset Management and Streaming Platform
**Project Code**: P11 | **Skill Track**: FSD Python  
**Institution**: ABES Engineering College | MCA 2nd Year  
**Prepared by**: Program Manager, EdTech, HCLTech  
**Git Repository**: `mca2-fsdpython-mediamerge`

---

## 1. Project Overview
MediaMerge is a unified enterprise platform designed for digital media asset lifecycle management, studio contract & intellectual property rights governance, automated royalty distribution, and secure content delivery with Digital Rights Management (DRM).

### All 12 Core Modules Implemented:
1. **Asset Metadata Management**: Ingestion, cataloging, format specs, and flexible EAV technical metadata.
2. **Search and Retrieval**: Faceted multi-attribute search across title, language, censor rating, and tags.
3. **Access Control and Permissions**: Role-Based Access Control (Admin, Producer, Content Manager, Rights Officer, Subscriber) and granular asset-level permissions.
4. **Asset Versioning and History**: Cryptographic SHA-256 version ledger with instant master rollback.
5. **Contract and Rights Management**: Studio registry (Dharma, YRF, T-Series, Zee Studios, Sun Pictures), licensing agreements, and territory controls.
6. **Royalty Calculation and Distribution**: Automated revenue-split calculation engine, 10% TDS deduction under Section 194J, and NEFT bank payout settlement.
7. **Sales Data Integration**: Raw multi-platform sales ledger tracking units streamed and gross revenue.
8. **Reporting and Analytics**: Executive KPI counters, storage analytics, and monthly revenue trajectories.
9. **User Registration and Authentication**: Secure salted password authentication, token exchange, and role assignments.
10. **Subscription Management and Billing**: Tiered plans (Standard to Enterprise), 1-click subscription activation, and GST tax invoice generation.
11. **Content Streaming and DRM**: Playback session negotiation, Widevine L1 token verification, and dynamic forensic watermarking (anti-screen recording deterrence).
12. **Recommendation Engine and Personalization**: Hybrid collaborative filtering, playback resume tracker, and user review feedback.

---

## 2. Technology Stack
- **Backend**: Python 3.12, Django 5.1 LTS, Django REST Framework (DRF), PyMySQL, ReportLab, Cryptography.
- **Frontend**: React 18, Vite, Bootstrap 5, Bootstrap Icons, Lucide Icons, Axios.
- **Database**: Dual Engine Support:
  - **MySQL 8.0**: Complete normalized 3NF DDL (`database/schema.sql`) and Indian-context seed script (`database/seed_data.sql`).
  - **SQLite3**: Pre-configured and migrated out-of-the-box (`backend/db.sqlite3`) for instant zero-dependency local execution.
- **Testing**: Pytest & pytest-django (100% passing across 9 test suites).

---

## 3. Project Directory Layout
```
mca2-fsdpython-mediamerge/
├── backend/                  # Django REST Framework application
│   ├── core/                 # Auth, Users, Roles, RBAC, load_seed_data command
│   ├── assets/               # Media assets, formats, categories, EAV metadata, versioning
│   ├── rights/               # Contracts, rights holders, sales, royalties, payouts
│   ├── streaming/            # DRM policies, streaming sessions, DRM token verification
│   ├── subscriptions/        # Plans, user subscriptions, GST billing invoices
│   ├── analytics/            # Dashboard KPIs, watch history, recommendations
│   ├── mediamerge_core/      # Django settings, root URLs, WSGI
│   ├── tests/                # Automated Pytest suite
│   ├── requirements.txt      # Python dependencies
│   ├── pytest.ini            # Pytest configuration
│   └── venv/                 # Pre-configured Python virtual environment
├── frontend/                 # React 18 application created with Vite
│   ├── src/
│   │   ├── components/       # UI screens for all 12 modules
│   │   ├── services/api.js   # Axios client for backend endpoints
│   │   ├── App.jsx           # Master application container
│   │   └── App.css           # High-tech dark glassmorphism styling
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite build configuration with API proxy
├── database/                 # Database scripts & exports
│   ├── schema.sql            # Normalized 3NF MySQL 8.0 DDL script
│   ├── seed_data.sql         # 100+ realistic Indian-context INSERT statements
│   ├── generate_data.py      # Automated seed dataset generator
│   └── csv_data/             # Seed data exported across all 25 tables in CSV format
├── docs/                     # Project documentation
│   ├── requirements.md       # Detailed module specifications
│   ├── wireframes.md         # ASCII & structural UI layouts
│   ├── api_documentation.md  # Complete RESTful endpoint guide
│   ├── er_diagram.md         # Mermaid ER diagram & 1:N / M:N relationships
│   ├── test_report.md        # Pytest test execution report
│   └── sprint_reviews/       # Agile reviews for Sprints 0, 1, 2, and 3
├── run_backend.bat           # 1-Click launcher for backend server
├── run_frontend.bat          # 1-Click launcher for frontend server
├── run_all.bat               # 1-Click launcher starting both servers
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore configuration
└── README.md                 # Project documentation
```

---

## 4. How to Run Locally

### Option A: 1-Click Startup (Recommended)
Double-click `run_all.bat` (or open a terminal in the project directory and run):
```cmd
run_all.bat
```
This launches both the Django REST backend (`http://127.0.0.1:8000`) and the React UI (`http://127.0.0.1:3000`).

---

### Option B: Manual Terminal Execution

#### 1. Start Django Backend Server:
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver 8000
```
Backend API will be live at `http://127.0.0.1:8000/api/`

#### 2. Start React Frontend Server:
In a separate terminal:
```bash
cd frontend
npm run dev
```
Open your browser at `http://localhost:3000`

---

## 5. Running Automated Tests
Run the test suite using pytest:
```bash
cd backend
.\venv\Scripts\pytest
```
Output:
```
============================== 9 passed in 2.54s ==============================
```

---

## 6. Pre-Seeded Test Credentials
All master accounts accept password: `password123` or `admin123`

| Full Name | Role | Email |
| :--- | :--- | :--- |
| **Aditya Vikram Sharma** | Admin | `aditya.admin@mediamerge.in` |
| **Karan Johar Singhania** | Producer | `karan.producer@dharmamedia.in` |
| **Pooja Hegde Iyer** | Content Manager | `pooja.curator@mediamerge.in` |
| **Sunita Narayanan** | Rights & Royalty Officer | `sunita.royalty@mediamerge.in` |
| **Aarav Gupta** | Subscriber | `aarav.gupta99@gmail.com` |

*(You can switch active roles anytime directly from the top navigation bar dropdown in the React app!)*

---

## 7. Connecting to MySQL 8.0 Server (Optional)
By default, the application runs immediately using SQLite with identical schema and pre-seeded Indian data.  
To switch to an external MySQL 8.0 instance:
1. Ensure MySQL Server is running on port 3306.
2. Execute the DDL & DML scripts:
   ```bash
   mysql -u root -p < database/schema.sql
   mysql -u root -p < database/seed_data.sql
   ```
3. Update `backend/.env`:
   ```env
   DB_ENGINE=mysql
   DB_NAME=mediamerge_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

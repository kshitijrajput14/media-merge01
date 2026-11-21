-- =====================================================================
-- MediaMerge - Integrated Media Asset Management and Streaming Platform
-- Database Definition Script (DDL)
-- Target RDBMS: MySQL 8.0+
-- Storage Engine: InnoDB | Character Set: utf8mb4 | Collation: utf8mb4_unicode_ci
-- Normalized relational schema (3NF) supporting all 12 modules
-- =====================================================================

CREATE DATABASE IF NOT EXISTS mediamerge_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mediamerge_db;

SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing tables if re-running
DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS user_ratings_reviews;
DROP TABLE IF EXISTS user_watch_history;
DROP TABLE IF EXISTS drm_tokens;
DROP TABLE IF EXISTS streaming_sessions;
DROP TABLE IF EXISTS billing_invoices;
DROP TABLE IF EXISTS user_subscriptions;
DROP TABLE IF EXISTS royalty_payouts;
DROP TABLE IF EXISTS royalty_calculations;
DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS contract_assets;
DROP TABLE IF EXISTS contracts;
DROP TABLE IF EXISTS asset_permissions;
DROP TABLE IF EXISTS asset_versions;
DROP TABLE IF EXISTS asset_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS asset_metadata;
DROP TABLE IF EXISTS media_assets;
DROP TABLE IF EXISTS subscription_plans;
DROP TABLE IF EXISTS rights_holders;
DROP TABLE IF EXISTS drm_policies;
DROP TABLE IF EXISTS media_formats;
DROP TABLE IF EXISTS media_categories;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

SET FOREIGN_KEY_CHECKS = 1;

-- ---------------------------------------------------------------------
-- 1. MODULE: ACCESS CONTROL & PERMISSIONS (MASTER TABLES)
-- ---------------------------------------------------------------------

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NULL,
    city VARCHAR(80) NULL,
    state VARCHAR(80) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_role ON users (role_id);
CREATE INDEX idx_users_city ON users (city);

-- ---------------------------------------------------------------------
-- 2. MODULE: ASSET METADATA MANAGEMENT (MASTER & LOOKUP TABLES)
-- ---------------------------------------------------------------------

CREATE TABLE media_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(60) NOT NULL UNIQUE,
    code VARCHAR(30) NOT NULL UNIQUE,
    description TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE media_formats (
    format_id INT AUTO_INCREMENT PRIMARY KEY,
    format_name VARCHAR(50) NOT NULL UNIQUE,
    resolution VARCHAR(30) NOT NULL,
    video_codec VARCHAR(30) NOT NULL,
    audio_codec VARCHAR(30) NOT NULL,
    container VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE drm_policies (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_name VARCHAR(80) NOT NULL UNIQUE,
    encryption_type VARCHAR(40) NOT NULL DEFAULT 'AES-128',
    allow_offline BOOLEAN NOT NULL DEFAULT FALSE,
    token_ttl_minutes INT NOT NULL DEFAULT 120,
    watermark_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    geo_restriction VARCHAR(100) NOT NULL DEFAULT 'IN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE rights_holders (
    rights_holder_id INT AUTO_INCREMENT PRIMARY KEY,
    legal_name VARCHAR(150) NOT NULL UNIQUE,
    trade_name VARCHAR(150) NULL,
    contact_person VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    city VARCHAR(80) NOT NULL,
    state VARCHAR(80) NOT NULL,
    gst_number VARCHAR(20) NULL UNIQUE,
    pan_number VARCHAR(15) NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE subscription_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(80) NOT NULL UNIQUE,
    plan_tier ENUM('Free', 'Standard', 'Premium', 'Enterprise') NOT NULL DEFAULT 'Standard',
    price_inr DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    billing_cycle_days INT NOT NULL DEFAULT 30,
    max_screens INT NOT NULL DEFAULT 1,
    video_quality VARCHAR(30) NOT NULL DEFAULT '1080p FHD',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(60) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 3. MODULE: ASSETS & REPOSITORIES (CORE TRANSACTIONS)
-- ---------------------------------------------------------------------

CREATE TABLE media_assets (
    asset_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    category_id INT NOT NULL,
    format_id INT NOT NULL,
    drm_policy_id INT NOT NULL,
    rights_holder_id INT NOT NULL,
    duration_seconds INT NOT NULL DEFAULT 0,
    file_size_mb DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    storage_path VARCHAR(255) NOT NULL,
    thumbnail_url VARCHAR(255) NULL,
    censor_rating VARCHAR(10) NOT NULL DEFAULT 'U/A 13+',
    release_year INT NOT NULL DEFAULT 2024,
    primary_language VARCHAR(40) NOT NULL DEFAULT 'Hindi',
    status ENUM('Draft', 'Review', 'Approved', 'Published', 'Archived') NOT NULL DEFAULT 'Draft',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_assets_category FOREIGN KEY (category_id) REFERENCES media_categories (category_id) ON DELETE RESTRICT,
    CONSTRAINT fk_assets_format FOREIGN KEY (format_id) REFERENCES media_formats (format_id) ON DELETE RESTRICT,
    CONSTRAINT fk_assets_drm FOREIGN KEY (drm_policy_id) REFERENCES drm_policies (policy_id) ON DELETE RESTRICT,
    CONSTRAINT fk_assets_rights_holder FOREIGN KEY (rights_holder_id) REFERENCES rights_holders (rights_holder_id) ON DELETE RESTRICT,
    CONSTRAINT fk_assets_creator FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_assets_title ON media_assets (title);
CREATE INDEX idx_assets_status ON media_assets (status);
CREATE INDEX idx_assets_category ON media_assets (category_id);
CREATE INDEX idx_assets_language ON media_assets (primary_language);
CREATE INDEX idx_assets_release_year ON media_assets (release_year);

CREATE TABLE asset_metadata (
    metadata_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    meta_key VARCHAR(80) NOT NULL,
    meta_value TEXT NOT NULL,
    data_type ENUM('string', 'number', 'boolean', 'json') NOT NULL DEFAULT 'string',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_meta_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT uq_asset_metakey UNIQUE (asset_id, meta_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_metadata_key ON asset_metadata (meta_key);

CREATE TABLE asset_tags (
    asset_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (asset_id, tag_id),
    CONSTRAINT fk_at_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT fk_at_tag FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 4. MODULE: ASSET VERSIONING & HISTORY
-- ---------------------------------------------------------------------

CREATE TABLE asset_versions (
    version_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    version_number VARCHAR(20) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size_mb DECIMAL(10,2) NOT NULL,
    checksum_sha256 VARCHAR(64) NOT NULL,
    change_summary VARCHAR(255) NULL,
    created_by INT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_versions_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT fk_versions_creator FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE RESTRICT,
    CONSTRAINT uq_asset_version UNIQUE (asset_id, version_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_versions_asset ON asset_versions (asset_id);

-- ---------------------------------------------------------------------
-- 5. MODULE: ACCESS CONTROL & PERMISSIONS (GRANULAR)
-- ---------------------------------------------------------------------

CREATE TABLE asset_permissions (
    permission_id INT AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    user_id INT NULL,
    role_id INT NULL,
    permission_type ENUM('view', 'edit', 'download', 'publish', 'delete') NOT NULL,
    granted_by INT NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_perm_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT fk_perm_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_perm_role FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE,
    CONSTRAINT fk_perm_granter FOREIGN KEY (granted_by) REFERENCES users (user_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_perm_asset_user ON asset_permissions (asset_id, user_id);

-- ---------------------------------------------------------------------
-- 6. MODULE: CONTRACT & RIGHTS MANAGEMENT
-- ---------------------------------------------------------------------

CREATE TABLE contracts (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_code VARCHAR(50) NOT NULL UNIQUE,
    rights_holder_id INT NOT NULL,
    contract_title VARCHAR(200) NOT NULL,
    contract_type ENUM('Exclusive Licensing', 'Non-Exclusive Licensing', 'Revenue Share', 'Original Production') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    territory VARCHAR(100) NOT NULL DEFAULT 'India, SAARC',
    terms_summary TEXT NULL,
    royalty_rate_percent DECIMAL(5,2) NOT NULL DEFAULT 15.00,
    status ENUM('Draft', 'Active', 'Terminated', 'Expired') NOT NULL DEFAULT 'Active',
    signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_contract_holder FOREIGN KEY (rights_holder_id) REFERENCES rights_holders (rights_holder_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_contracts_holder ON contracts (rights_holder_id);
CREATE INDEX idx_contracts_status ON contracts (status);

CREATE TABLE contract_assets (
    contract_asset_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    asset_id INT NOT NULL,
    exclusivity BOOLEAN NOT NULL DEFAULT TRUE,
    royalty_split_percent DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    CONSTRAINT fk_ca_contract FOREIGN KEY (contract_id) REFERENCES contracts (contract_id) ON DELETE CASCADE,
    CONSTRAINT fk_ca_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE RESTRICT,
    CONSTRAINT uq_contract_asset UNIQUE (contract_id, asset_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 7. MODULE: SALES DATA INTEGRATION & ROYALTY CALCULATION
-- ---------------------------------------------------------------------

CREATE TABLE sales_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_code VARCHAR(60) NOT NULL UNIQUE,
    contract_id INT NOT NULL,
    asset_id INT NOT NULL,
    platform_name VARCHAR(80) NOT NULL DEFAULT 'MediaMerge OTT',
    territory VARCHAR(60) NOT NULL DEFAULT 'India',
    units_streamed INT NOT NULL DEFAULT 1,
    gross_revenue_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    platform_fee_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    net_revenue_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_st_contract FOREIGN KEY (contract_id) REFERENCES contracts (contract_id) ON DELETE RESTRICT,
    CONSTRAINT fk_st_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_sales_contract ON sales_transactions (contract_id);
CREATE INDEX idx_sales_asset ON sales_transactions (asset_id);
CREATE INDEX idx_sales_date ON sales_transactions (transaction_date);

CREATE TABLE royalty_calculations (
    calculation_id INT AUTO_INCREMENT PRIMARY KEY,
    calculation_code VARCHAR(50) NOT NULL UNIQUE,
    contract_id INT NOT NULL,
    rights_holder_id INT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    gross_sales_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    royalty_rate_percent DECIMAL(5,2) NOT NULL,
    calculated_royalty_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax_deduction_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    net_payable_inr DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    payment_status ENUM('Calculated', 'Approved', 'Paid', 'Disputed') NOT NULL DEFAULT 'Calculated',
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rc_contract FOREIGN KEY (contract_id) REFERENCES contracts (contract_id) ON DELETE RESTRICT,
    CONSTRAINT fk_rc_holder FOREIGN KEY (rights_holder_id) REFERENCES rights_holders (rights_holder_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_rc_contract ON royalty_calculations (contract_id);
CREATE INDEX idx_rc_holder ON royalty_calculations (rights_holder_id);
CREATE INDEX idx_rc_status ON royalty_calculations (payment_status);

CREATE TABLE royalty_payouts (
    payout_id INT AUTO_INCREMENT PRIMARY KEY,
    calculation_id INT NOT NULL,
    payout_reference VARCHAR(60) NOT NULL UNIQUE,
    payment_mode ENUM('NEFT', 'RTGS', 'IMPS', 'UPI', 'Direct Bank Transfer') NOT NULL DEFAULT 'NEFT',
    transaction_date DATE NOT NULL,
    amount_inr DECIMAL(12,2) NOT NULL,
    status ENUM('Initiated', 'Completed', 'Failed') NOT NULL DEFAULT 'Completed',
    remarks VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rp_calc FOREIGN KEY (calculation_id) REFERENCES royalty_calculations (calculation_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 8. MODULE: SUBSCRIPTION MANAGEMENT & BILLING
-- ---------------------------------------------------------------------

CREATE TABLE user_subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('Active', 'Expired', 'Cancelled', 'Pending') NOT NULL DEFAULT 'Active',
    auto_renew BOOLEAN NOT NULL DEFAULT TRUE,
    payment_method VARCHAR(50) NOT NULL DEFAULT 'Razorpay UPI',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_us_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_us_plan FOREIGN KEY (plan_id) REFERENCES subscription_plans (plan_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_us_user ON user_subscriptions (user_id);
CREATE INDEX idx_us_status ON user_subscriptions (status);

CREATE TABLE billing_invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    subscription_id INT NOT NULL,
    user_id INT NOT NULL,
    base_amount_inr DECIMAL(10,2) NOT NULL,
    gst_rate_percent DECIMAL(5,2) NOT NULL DEFAULT 18.00,
    gst_amount_inr DECIMAL(10,2) NOT NULL,
    total_amount_inr DECIMAL(10,2) NOT NULL,
    payment_status ENUM('Paid', 'Pending', 'Failed', 'Refunded') NOT NULL DEFAULT 'Paid',
    invoice_date DATE NOT NULL,
    paid_date DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bi_sub FOREIGN KEY (subscription_id) REFERENCES user_subscriptions (subscription_id) ON DELETE CASCADE,
    CONSTRAINT fk_bi_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_bi_user ON billing_invoices (user_id);
CREATE INDEX idx_bi_invoice_date ON billing_invoices (invoice_date);

-- ---------------------------------------------------------------------
-- 9. MODULE: CONTENT STREAMING & DRM
-- ---------------------------------------------------------------------

CREATE TABLE streaming_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    session_token VARCHAR(100) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    watch_duration_seconds INT NOT NULL DEFAULT 0,
    playback_quality VARCHAR(20) NOT NULL DEFAULT '1080p',
    device_type VARCHAR(50) NOT NULL DEFAULT 'Desktop Web',
    ip_address VARCHAR(45) NOT NULL DEFAULT '127.0.0.1',
    completion_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_ss_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_ss_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_ss_user_asset ON streaming_sessions (user_id, asset_id);
CREATE INDEX idx_ss_start_time ON streaming_sessions (start_time);

CREATE TABLE drm_tokens (
    drm_token_id INT AUTO_INCREMENT PRIMARY KEY,
    token_string VARCHAR(128) NOT NULL UNIQUE,
    session_id INT NOT NULL,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    license_type ENUM('StreamingPlayback', 'OfflineRental', 'EditorialPreview') NOT NULL DEFAULT 'StreamingPlayback',
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_dt_session FOREIGN KEY (session_id) REFERENCES streaming_sessions (session_id) ON DELETE CASCADE,
    CONSTRAINT fk_dt_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_dt_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_dt_token ON drm_tokens (token_string);
CREATE INDEX idx_dt_expires ON drm_tokens (expires_at);

-- ---------------------------------------------------------------------
-- 10. MODULE: RECOMMENDATION ENGINE & PERSONALIZATION
-- ---------------------------------------------------------------------

CREATE TABLE user_watch_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    last_playback_position_seconds INT NOT NULL DEFAULT 0,
    total_duration_seconds INT NOT NULL DEFAULT 0,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_uwh_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_uwh_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT uq_user_asset_history UNIQUE (user_id, asset_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE user_ratings_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_urr_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_urr_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT uq_user_asset_rating UNIQUE (user_id, asset_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    score DECIMAL(4,3) NOT NULL DEFAULT 0.850,
    recommendation_algorithm VARCHAR(80) NOT NULL DEFAULT 'CollaborativeFiltering+GenreMatch',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rec_user FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_rec_asset FOREIGN KEY (asset_id) REFERENCES media_assets (asset_id) ON DELETE CASCADE,
    CONSTRAINT uq_user_rec UNIQUE (user_id, asset_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_rec_user_score ON recommendations (user_id, score DESC);

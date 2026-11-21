import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "csv_data")
os.makedirs(CSV_DIR, exist_ok=True)
SQL_FILE = os.path.join(BASE_DIR, "seed_data.sql")

# 1. ROLES (6 rows)
roles_data = [
    (1, "Admin", "System administrator with full platform access"),
    (2, "Producer", "Media creator and executive overseeing asset production and distribution"),
    (3, "Content Manager", "Curator managing asset metadata, review, publishing, and scheduling"),
    (4, "Rights & Royalty Officer", "Finance and legal manager auditing rights, sales, and royalties"),
    (5, "Distributor", "Partner distributor accessing licensed streaming syndication"),
    (6, "Subscriber", "End-user with streaming subscription access")
]

# 2. USERS (15 rows) - Indian Context + Hashed Passwords
# PBKDF2 placeholder hash for test accounts: 'pbkdf2_sha256$600000$dummySalt$e7f8...dummyhash...'
HASH_PW = "pbkdf2_sha256$600000$mediamergeSalt$b9c7e096414f48e285a73e449a56c078e87ad60773b064c1b97950541cf354e1"

users_data = [
    (1, 1, "Aditya Vikram Sharma", "aditya.admin@mediamerge.in", HASH_PW, "+91-9811023456", "New Delhi", "Delhi", True, "2024-01-10 10:00:00"),
    (2, 2, "Karan Johar Singhania", "karan.producer@dharmamedia.in", HASH_PW, "+91-9820011223", "Mumbai", "Maharashtra", True, "2024-01-15 11:30:00"),
    (3, 2, "Anurag Kashyap Verma", "anurag.indie@gangsofcinema.in", HASH_PW, "+91-9820099887", "Mumbai", "Maharashtra", True, "2024-01-20 14:15:00"),
    (4, 3, "Pooja Hegde Iyer", "pooja.curator@mediamerge.in", HASH_PW, "+91-9844055667", "Bengaluru", "Karnataka", True, "2024-02-01 09:00:00"),
    (5, 3, "Rohan Mukhopadhyay", "rohan.content@mediamerge.in", HASH_PW, "+91-9830012345", "Kolkata", "West Bengal", True, "2024-02-05 10:45:00"),
    (6, 4, "Sunita Narayanan", "sunita.royalty@mediamerge.in", HASH_PW, "+91-9840077889", "Chennai", "Tamil Nadu", True, "2024-02-10 16:20:00"),
    (7, 4, "Vikramaditya Rao", "vikram.finance@mediamerge.in", HASH_PW, "+91-9849033445", "Hyderabad", "Telangana", True, "2024-02-12 11:00:00"),
    (8, 5, "Manoj Bajpayee Bajpai", "manoj.distrib@penindia.com", HASH_PW, "+91-9821044556", "Mumbai", "Maharashtra", True, "2024-02-15 13:30:00"),
    (9, 6, "Aarav Gupta", "aarav.gupta99@gmail.com", HASH_PW, "+91-9810123456", "Noida", "Uttar Pradesh", True, "2024-03-01 18:00:00"),
    (10, 6, "Ananya Reddy", "ananya.reddy@yahoo.co.in", HASH_PW, "+91-9848011223", "Hyderabad", "Telangana", True, "2024-03-05 20:15:00"),
    (11, 6, "Rohan Deshmukh", "rohan.deshmukh@outlook.com", HASH_PW, "+91-9823055443", "Pune", "Maharashtra", True, "2024-03-10 12:00:00"),
    (12, 6, "Deepika Srinivasan", "deepika.s@gmail.com", HASH_PW, "+91-9841099881", "Chennai", "Tamil Nadu", True, "2024-03-15 19:45:00"),
    (13, 6, "Kabir Mehta", "kabir.mehta@hotmail.com", HASH_PW, "+91-9871033221", "Gurugram", "Haryana", True, "2024-03-20 21:10:00"),
    (14, 6, "Meera Nambiar", "meera.nambiar@gmail.com", HASH_PW, "+91-9847066554", "Kochi", "Kerala", True, "2024-04-01 17:30:00"),
    (15, 6, "Tanmay Bhatia", "tanmay.bhatia@gmail.com", HASH_PW, "+91-9818044332", "Jaipur", "Rajasthan", True, "2024-04-05 22:00:00"),
    # Edge case 1: duplicate-looking name with different email & city
    (16, 6, "Aarav Gupta", "aarav.gupta.delhi@gmail.com", HASH_PW, "+91-9810199999", "New Delhi", "Delhi", True, "2024-04-10 10:00:00"),
    # Edge case 2: null phone & city (empty optional fields)
    (17, 6, "Sneha Patel", "sneha.patel.anonymous@gmail.com", HASH_PW, None, None, None, True, "2024-04-12 14:00:00")
]

# 3. MEDIA CATEGORIES (10 rows)
categories_data = [
    (1, "Feature Film", "FEATURE_FILM", "Full-length theatrical and streaming narrative motion pictures", True),
    (2, "Web Series", "WEB_SERIES", "Episodic narrative dramas, comedies, and mini-series", True),
    (3, "Documentary", "DOCUMENTARY", "Non-fiction educational, wildlife, and biographical features", True),
    (4, "Music Video", "MUSIC_VIDEO", "Official musical tracks and synchronized video releases", True),
    (5, "Original Soundtrack", "OST_AUDIO", "Standalone high-fidelity musical scores and audio tracks", True),
    (6, "Trailer & Promo", "PROMO_TRAILER", "Teaser trailers, launch promos, and marketing cutdowns", True),
    (7, "Behind the Scenes", "BTS_FEATURE", "Exclusive making-of reels, director interviews, and B-roll", True),
    (8, "Short Film", "SHORT_FILM", "Curated independent cinema under 45 minutes", True),
    (9, "Podcast & Talk Show", "PODCAST", "Spoken-word cultural talks and entertainment discussions", True),
    (10, "4K Archival Classic", "ARCHIVAL", "Digitally restored heritage cinema of Indian golden age", True)
]

# 4. MEDIA FORMATS (10 rows)
formats_data = [
    (1, "4K UHD Master (ProRes)", "3840x2160", "Apple ProRes 422 HQ", "LPCM 24-bit 5.1", "MOV", True),
    (2, "4K UHD Streaming (HEVC/H.265)", "3840x2160", "HEVC / H.265 Main 10", "Dolby Digital Plus E-AC-3", "MP4", True),
    (3, "1080p FHD High-Bitrate (AVC/H.264)", "1920x1080", "AVC / H.264 High@L4.1", "AAC-LC Stereo 320kbps", "MP4", True),
    (4, "1080p FHD Broadcast Clean", "1920x1080", "XDCAM HD422", "PCM 24-bit 48kHz", "MXF", True),
    (5, "720p HD Mobile Optimized", "1280x720", "AVC / H.264 Main", "AAC-LC 128kbps", "MP4", True),
    (6, "480p SD Low-Bandwidth", "854x480", "AVC / H.264 Baseline", "AAC-LC 96kbps", "MP4", True),
    (7, "Lossless Studio Audio (FLAC)", "N/A", "None", "FLAC 24-bit 96kHz", "FLAC", True),
    (8, "High-Res Master Audio (WAV)", "N/A", "None", "LPCM 24-bit 48kHz", "WAV", True),
    (9, "Streaming Audio (AAC)", "N/A", "None", "AAC-LC 256kbps", "M4A", True),
    (10, "Compact Audio (MP3 320k)", "N/A", "None", "MP3 320kbps CBR", "MP3", True)
]

# 5. DRM POLICIES (10 rows)
drm_data = [
    (1, "Widevine L1 + PlayReady UHD", "AES-128-CBC", True, 240, True, "IN,SAARC"),
    (2, "Widevine L3 Standard Web", "AES-128-CTR", False, 120, True, "IN"),
    (3, "FairPlay iOS Native Secure", "AES-128-CBC", True, 360, True, "GLOBAL"),
    (4, "ClearKey Tokenized Preview", "AES-128-CTR", False, 30, False, "IN"),
    (5, "Watermarked Editorial Screener", "AES-256", False, 60, True, "INTERNAL_ONLY"),
    (6, "Festival Licensing Restricted", "AES-128-CBC", False, 180, True, "IN,UK,US"),
    (7, "Syndication Partner DRM", "AES-128-CTR", True, 720, False, "IN,AE,SG"),
    (8, "Open Educational License (No DRM)", "NONE", True, 1440, False, "GLOBAL"),
    (9, "High-Security Master Vault DRM", "AES-256-GCM", False, 15, True, "OFFICE_IP_ONLY"),
    (10, "Rental 48-Hour Auto-Revoke", "AES-128-CBC", True, 2880, True, "IN")
]

# 6. RIGHTS HOLDERS (12 rows) - Realistic Indian Studios & Labels
rights_holders_data = [
    (1, "Dharma Productions Media Pvt Ltd", "Dharma Productions", "Hiroo Yash Johar", "licensing@dharmamedia.in", "+91-22-67891234", "Mumbai", "Maharashtra", "27AAACD1234F1Z5", "AAACD1234F"),
    (2, "Yash Raj Films Digital Pvt Ltd", "YRF Digital", "Akshaye Widhani", "distribution@yrf.in", "+91-22-26785000", "Mumbai", "Maharashtra", "27AAACY5678G1Z2", "AAACY5678G"),
    (3, "Super Cassettes Industries Pvt Ltd", "T-Series Entertainment", "Bhushan Kumar Dua", "rights@tseries.net", "+91-11-23456789", "Noida", "Uttar Pradesh", "09AAACS9876H1Z8", "AAACS9876H"),
    (4, "Excel Entertainment LLP", "Excel Cinema", "Ritesh Sidhwani", "legal@excelmovies.com", "+91-22-45678901", "Mumbai", "Maharashtra", "27AAAEE4321J1Z3", "AAAEE4321J"),
    (5, "Sun TV Network Limited", "Sun Pictures", "Kalanithi Maran", "ott.rights@suntv.in", "+91-44-28456789", "Chennai", "Tamil Nadu", "33AAACS1122K1Z9", "AAACS1122K"),
    (6, "Geetha Arts Production LLP", "Geetha Arts", "Allu Aravind", "licensing@geethaarts.in", "+91-40-23451122", "Hyderabad", "Telangana", "36AAACG3344L1Z7", "AAACG3344L"),
    (7, "Red Chillies VFX & Entertainment", "Red Chillies Ent", "Venky Mysore", "ipr@redchillies.com", "+91-22-66998800", "Mumbai", "Maharashtra", "27AAACR5566M1Z4", "AAACR5566M"),
    (8, "Zee Entertainment Enterprises Ltd", "Zee Studios", "Punit Goenka", "syndication@zee.esselgroup.com", "+91-22-71061234", "Mumbai", "Maharashtra", "27AAACZ7788N1Z1", "AAACZ7788N"),
    (9, "SVF Entertainment Pvt Ltd", "SVF Cinema", "Shrikant Mohta", "digital@svf.in", "+91-33-24631234", "Kolkata", "West Bengal", "19AAACS8899P1Z6", "AAACS8899P"),
    (10, "Saregama India Limited", "Saregama Music", "Vikram Mehra", "musicrights@saregama.com", "+91-33-22871234", "Kolkata", "West Bengal", "19AAACS0011Q1Z0", "AAACS0011Q"),
    (11, "Hombale Films LLP", "Hombale Digital", "Vijay Kiragandur", "distribution@hombale.in", "+91-80-26781234", "Bengaluru", "Karnataka", "29AAACH2233R1Z5", "AAACH2233R"),
    (12, "E4 Entertainment South", "E4 Indie", "Mukesh R. Mehta", "e4south@e4entertainment.com", "+91-484-2391234", "Kochi", "Kerala", "32AAACE4455S1Z3", "AAACE4455S")
]

# 7. SUBSCRIPTION PLANS (6 rows)
plans_data = [
    (1, "MediaMerge Free Tier", "Free", 0.00, 365, 1, "720p HD with Ads", True),
    (2, "Standard Mobile Monthly", "Standard", 149.00, 30, 1, "720p HD", True),
    (3, "Standard All-Device Monthly", "Standard", 299.00, 30, 2, "1080p FHD", True),
    (4, "Premium Cinema 4K Monthly", "Premium", 499.00, 30, 4, "4K UHD + Dolby Atmos", True),
    (5, "Premium Cinema 4K Annual", "Premium", 1499.00, 365, 4, "4K UHD + Dolby Atmos", True),
    (6, "Enterprise Studio Screening Pass", "Enterprise", 4999.00, 90, 10, "Master Quality ProRes / 4K", True)
]

# 8. TAGS (15 rows)
tags_data = [
    (1, "Bollywood Blockbuster", "bollywood-blockbuster"),
    (2, "South Indian Action", "south-action"),
    (3, "Critically Acclaimed", "critically-acclaimed"),
    (4, "Romantic Comedy", "rom-com"),
    (5, "Crime Thriller", "crime-thriller"),
    (6, "Historical Epic", "historical-epic"),
    (7, "Indie Festival Winner", "indie-festival"),
    (8, "Family Drama", "family-drama"),
    (9, "Classical Raga", "classical-raga"),
    (10, "Pop Fusion", "pop-fusion"),
    (11, "National Award Winner", "national-award"),
    (12, "4K Restored", "4k-restored"),
    (13, "Biopic", "biopic"),
    (14, "Sci-Fi Fantasy", "sci-fi"),
    (15, "Trending Now", "trending-now")
]

# 9. MEDIA ASSETS (60 rows) - Realistic Indian titles
titles_pool = [
    ("Shershaah: The Kargil Legend", 1, 2, 1, 1, 8100, 4200.50, "U/A 13+", 2024, "Hindi", "Published"),
    ("Brahmastra: Part One Shiva", 1, 1, 1, 1, 9900, 6800.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Pathaan: Mission Shadow", 1, 2, 1, 2, 8760, 4500.20, "U/A 16+", 2024, "Hindi", "Published"),
    ("Jawan: The Vigilante Soldier", 1, 1, 3, 7, 10140, 7100.80, "U/A 16+", 2024, "Hindi", "Published"),
    ("Kantara: A Legend Divine", 1, 2, 1, 11, 8880, 4350.00, "U/A 16+", 2024, "Kannada", "Published"),
    ("KGF: Chapter 2 Gold Mines", 1, 1, 1, 11, 10080, 7500.00, "U/A 16+", 2024, "Kannada", "Published"),
    ("RRR: Rise Roar Revolt", 1, 1, 1, 6, 11220, 8200.00, "U/A 16+", 2024, "Telugu", "Published"),
    ("Pushpa: The Wildfire Rise", 1, 2, 1, 6, 10740, 5100.00, "U/A 16+", 2024, "Telugu", "Published"),
    ("Ponniyin Selvan: Kingdom Part 1", 1, 1, 1, 5, 10020, 6900.40, "U/A 13+", 2024, "Tamil", "Published"),
    ("Vikram: Ghost Syndicate", 1, 2, 1, 5, 10380, 5400.00, "A", 2024, "Tamil", "Published"),
    ("The Elephant Whisperers", 3, 2, 8, 4, 2460, 1200.00, "U", 2024, "Tamil", "Published"),
    ("Gully Boy: Voice of the Streets", 1, 3, 2, 4, 9180, 3100.00, "U/A 16+", 2024, "Hindi", "Published"),
    ("Mirzapur Chronicles: S03", 2, 2, 1, 4, 32400, 18500.00, "A", 2024, "Hindi", "Published"),
    ("Panchayat: Phulera Diaries S03", 2, 3, 2, 8, 21600, 9400.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Sacred Games: Mumbai Noir S02", 2, 2, 1, 7, 28800, 16200.00, "A", 2024, "Hindi", "Published"),
    ("Farzi: The Counterfeit Artist", 2, 2, 1, 8, 31200, 17800.00, "U/A 16+", 2024, "Hindi", "Published"),
    ("Kesariya: Romantic Raga Track", 4, 3, 2, 1, 275, 450.00, "U", 2024, "Hindi", "Published"),
    ("Naatu Naatu: Oscar Winning Master", 4, 1, 1, 6, 260, 980.00, "U", 2024, "Telugu", "Published"),
    ("Jhoome Jo Pathaan: Groove Anthem", 4, 3, 2, 2, 215, 380.00, "U", 2024, "Hindi", "Published"),
    ("Apna Bana Le: Soulful Melody", 4, 3, 2, 8, 260, 410.00, "U", 2024, "Hindi", "Published"),
    ("Deva Deva: Spiritual Resonance", 4, 2, 1, 1, 290, 520.00, "U", 2024, "Hindi", "Published"),
    ("Aparajito: Ray Restored Masterpiece", 10, 1, 9, 9, 7200, 9200.00, "U", 2024, "Bengali", "Published"),
    ("Pather Panchali: 4K Heritage Print", 10, 1, 9, 9, 7500, 9500.00, "U", 2024, "Bengali", "Published"),
    ("Mughal-E-Azam: Coloured 4K Symphony", 10, 1, 9, 10, 11820, 10500.00, "U", 2024, "Urdu", "Published"),
    ("Sholay: 70mm Stereophonic Classic", 10, 1, 1, 8, 12240, 11200.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Jaane Bhi Do Yaaro: Cult Satire", 10, 3, 2, 8, 7920, 2800.00, "U", 2024, "Hindi", "Published"),
    ("Lootere: High Seas Hijack S01", 2, 2, 1, 8, 25200, 14200.00, "A", 2024, "Hindi", "Published"),
    ("Scam 2003: Telgi Stamp Story", 2, 3, 2, 8, 28800, 12500.00, "U/A 16+", 2024, "Hindi", "Published"),
    ("Kantara Folklore: Audio Symphony", 5, 7, 8, 11, 3600, 850.00, "U", 2024, "Kannada", "Published"),
    ("Coke Studio Bharat: Season 02 Master", 5, 8, 8, 10, 4800, 1200.00, "U", 2024, "Hindi", "Published"),
    ("Sounds of the Himalayas: Ambient Folk", 9, 7, 8, 10, 5400, 920.00, "U", 2024, "Hindi", "Published"),
    ("Filmmaker's Roundtable 2024", 9, 3, 4, 4, 5800, 1900.00, "U", 2024, "English", "Published"),
    ("The Great Indian Railway Odyssey", 3, 2, 2, 8, 5400, 2900.00, "U", 2024, "English", "Published"),
    ("Wild Karnataka: Tiger Territory", 3, 1, 1, 11, 3300, 5800.00, "U", 2024, "English", "Published"),
    ("Dharmendra: The Action Star Journey", 3, 3, 2, 10, 4800, 1800.00, "U", 2024, "Hindi", "Published"),
    ("Chupke Chupke: Vintage Comedy Cut", 1, 3, 2, 10, 8100, 2400.00, "U", 2024, "Hindi", "Published"),
    ("Gol Maal (1979): Hrishikesh Delight", 1, 3, 2, 10, 7800, 2300.00, "U", 2024, "Hindi", "Published"),
    ("Anand: Babu Moshai 4K Remaster", 10, 1, 9, 10, 7320, 8900.00, "U", 2024, "Hindi", "Published"),
    ("Taare Zameen Par: Special Edition", 1, 3, 2, 8, 9900, 3400.00, "U", 2024, "Hindi", "Published"),
    ("Dangal: Wrestling Glory", 1, 2, 1, 8, 9660, 4800.00, "U", 2024, "Hindi", "Published"),
    ("Chak De! India: Hockey Dreams", 1, 2, 1, 2, 9180, 4200.00, "U", 2024, "Hindi", "Published"),
    ("Zindagi Na Milegi Dobara: Spain Trip", 1, 2, 1, 4, 9300, 4600.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Dil Chahta Hai: Goa Forever", 1, 3, 2, 4, 10980, 3900.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Gangs of Wasseypur: Uncut Director Cut", 1, 2, 5, 3, 19200, 11200.00, "A", 2024, "Hindi", "Published"),
    ("Satya: Underworld Classic Remastered", 1, 3, 2, 3, 10200, 3600.00, "A", 2024, "Hindi", "Published"),
    ("Kaagaz Ke Phool: Guru Dutt Cinema", 10, 1, 9, 10, 8880, 9400.00, "U", 2024, "Hindi", "Published"),
    ("Awaara (1951): Raj Kapoor Milestone", 10, 1, 9, 10, 10200, 9800.00, "U", 2024, "Hindi", "Published"),
    ("Mahanagar: The Big City (Ray)", 10, 1, 9, 9, 7860, 8700.00, "U", 2024, "Bengali", "Published"),
    ("Charulata: The Lonely Wife", 10, 1, 9, 9, 7020, 8200.00, "U", 2024, "Bengali", "Published"),
    ("Kumbalangi Nights: Backwater Tales", 1, 2, 1, 12, 8100, 3900.00, "U/A 13+", 2024, "Malayalam", "Published"),
    ("Jallikattu: The Rogue Bull", 8, 2, 1, 12, 5460, 3200.00, "A", 2024, "Malayalam", "Published"),
    ("The Great Indian Kitchen", 1, 3, 2, 12, 6000, 2700.00, "U/A 13+", 2024, "Malayalam", "Published"),
    ("Super Deluxe: Chennai Stories", 1, 2, 1, 5, 10560, 5200.00, "A", 2024, "Tamil", "Published"),
    ("Asuran: Blood Oath", 1, 2, 1, 5, 8460, 4100.00, "A", 2024, "Tamil", "Published"),
    ("Karnan: The Rebellion", 1, 2, 1, 5, 9480, 4700.00, "U/A 16+", 2024, "Tamil", "Published"),
    ("MediaMerge Tech Keynote 2024", 6, 3, 4, 1, 1800, 650.00, "U", 2024, "English", "Published"),
    ("Behind The Scenes: VFX Magic of Brahmastra", 7, 3, 2, 7, 2400, 1100.00, "U", 2024, "Hindi", "Published"),
    ("Indian Cinema Evolution 1913-2024", 3, 2, 2, 10, 7200, 3800.00, "U", 2024, "English", "Published"),
    ("Indie Voices Podcast: Episode 01", 9, 10, 8, 3, 3600, 150.00, "U/A 13+", 2024, "Hindi", "Published"),
    ("Draft Feature Screening Asset 60", 1, 3, 5, 2, 6000, 2500.00, "U/A 13+", 2024, "Hindi", "Draft")
]

# Edge case 3: Asset 61 with Maximum length text description and empty optional fields
edge_asset = ("A" * 195, 1, 3, 2, 1, 3600, 1200.0, "U", 2025, "Hindi", "Draft")

assets_data = []
creator_ids = [1, 2, 3, 4, 5]
for idx, item in enumerate(titles_pool, start=1):
    title, cat_id, fmt_id, drm_id, rh_id, duration, size, censor, year, lang, status = item
    desc = f"Official production release of {title}. High quality master encode configured for streaming."
    storage = f"/storage/vault/{year}/{cat_id}/{idx}_{title.lower()[:15].replace(' ', '_')}.mp4"
    thumb = f"https://cdn.mediamerge.in/thumbs/{idx}_{cat_id}.jpg"
    creator = random.choice(creator_ids)
    created_at = f"2024-{random.randint(1,10):02d}-{random.randint(1,25):02d} 10:00:00"
    assets_data.append((idx, title, desc, cat_id, fmt_id, drm_id, rh_id, duration, size, storage, thumb, censor, year, lang, status, creator, created_at))

# Add Edge case asset 61
assets_data.append((61, "Z_EDGE_ASSET_MAX_TITLE_" + ("X"*160), "Detailed extensive synopsis "*50, 1, 3, 2, 1, 7200, 3500.00, "/storage/vault/edge/asset_61.mp4", None, "U", 2026, "Hindi", "Draft", 1, "2026-01-01 12:00:00"))

# 10. ASSET METADATA (60+ rows)
metadata_keys = [
    ("aspect_ratio", ["16:9", "2.39:1", "1.85:1", "4:3"]),
    ("audio_channels", ["5.1 Surround", "Stereo 2.0", "Dolby Atmos 7.1.4"]),
    ("frame_rate", ["24 fps", "25 fps", "29.97 fps", "60 fps"]),
    ("color_space", ["BT.709", "BT.2020 HDR", "DCI-P3"]),
    ("subtitles_available", ["Hindi, English", "Tamil, Telugu, English", "Bengali, English", "English Only"])
]

metadata_data = []
m_id = 1
for a in assets_data[:50]:
    aid = a[0]
    for mk, vals in metadata_keys:
        val = random.choice(vals)
        metadata_data.append((m_id, aid, mk, val, "string", a[16]))
        m_id += 1

# 11. ASSET TAGS (Many-to-Many: 90 rows)
asset_tags_data = []
for a in assets_data[:50]:
    aid = a[0]
    chosen_tags = random.sample(range(1, 16), 2)
    for tid in chosen_tags:
        asset_tags_data.append((aid, tid))

# 12. ASSET VERSIONS (65 rows)
versions_data = []
v_id = 1
for a in assets_data:
    aid = a[0]
    versions_data.append((v_id, aid, "v1.0.0", a[9], a[8], f"sha256_{random.randint(100000, 999999)}abcde", "Initial production master ingestion", a[15], True, a[16]))
    v_id += 1
# Add v1.1.0 for some assets
for a in assets_data[:10]:
    versions_data.append((v_id, a[0], "v1.1.0", a[9].replace(".mp4", "_v1.1.mp4"), a[8] + 50.0, f"sha256_{random.randint(100000, 999999)}revised", "Audio remaster and color grade correction", a[15], False, "2024-11-01 15:00:00"))
    v_id += 1

# 13. ASSET PERMISSIONS (55 rows)
perm_data = []
p_id = 1
for a in assets_data[:40]:
    perm_data.append((p_id, a[0], random.choice([2, 3, 4, 5, 8]), None, "view", 1, "2024-02-01 10:00:00"))
    p_id += 1
for a in assets_data[:15]:
    perm_data.append((p_id, a[0], None, 2, "edit", 1, "2024-02-01 10:00:00"))
    p_id += 1

# 14. CONTRACTS (15 rows)
contracts_data = [
    (1, "CNT-2024-DHRM-001", 1, "Dharma Premium Blockbusters Exclusive Deal 2024-2026", "Exclusive Licensing", "2024-01-01", "2026-12-31", "India, SAARC", "Full SVOD rights for tier 1 releases", 18.50, "Active", "2024-01-05 10:00:00"),
    (2, "CNT-2024-YRF-002", 2, "YRF Action Syndicate Digital Distribution Agreement", "Exclusive Licensing", "2024-01-10", "2026-06-30", "India, Middle East", "Streaming rights for theatrical releases", 20.00, "Active", "2024-01-12 11:30:00"),
    (3, "CNT-2024-TSR-003", 3, "T-Series Music & OST Audio Syndication Master", "Revenue Share", "2024-02-01", "2027-01-31", "Global", "Complete music catalogue streaming split", 12.00, "Active", "2024-02-02 14:00:00"),
    (4, "CNT-2024-EXC-004", 4, "Excel Entertainment Web Series & Drama Contract", "Original Production", "2024-02-15", "2026-02-14", "India", "Original series co-production", 15.00, "Active", "2024-02-18 16:00:00"),
    (5, "CNT-2024-SUN-005", 5, "Sun Pictures South Regional Blockbuster License", "Non-Exclusive Licensing", "2024-03-01", "2025-08-31", "South India, UAE, Malaysia", "Tamil blockbusters streaming package", 16.50, "Active", "2024-03-02 12:00:00"),
    (6, "CNT-2024-GTH-006", 6, "Geetha Arts Telugu Premiere Rights Agreement", "Exclusive Licensing", "2024-03-10", "2026-03-09", "India, USA, Australia", "Telugu theatrical slate digital rights", 17.00, "Active", "2024-03-15 15:30:00"),
    (7, "CNT-2024-RCH-007", 7, "Red Chillies Action & Sci-Fi Syndication Rights", "Exclusive Licensing", "2024-04-01", "2026-12-31", "Global", "Global streaming and VFX rights", 19.00, "Active", "2024-04-05 11:00:00"),
    (8, "CNT-2024-ZEE-008", 8, "Zee Studios Multi-Language Slate Distribution", "Non-Exclusive Licensing", "2024-04-15", "2025-12-31", "India", "Catalog and new releases distribution", 14.00, "Active", "2024-04-20 17:00:00"),
    (9, "CNT-2024-SVF-009", 9, "SVF Bengali Heritage & Modern Cinema Package", "Exclusive Licensing", "2024-05-01", "2027-04-30", "India, Bangladesh", "Bengali classic and contemporary package", 15.00, "Active", "2024-05-05 10:30:00"),
    (10, "CNT-2024-SRG-010", 10, "Saregama Golden Era Restored Cinema Catalog", "Exclusive Licensing", "2024-05-10", "2028-05-09", "Global", "Archival classics 4K streaming rights", 10.00, "Active", "2024-05-12 14:45:00"),
    (11, "CNT-2024-HMB-011", 11, "Hombale Films Pan-India Franchise Agreement", "Exclusive Licensing", "2024-06-01", "2026-12-31", "Global", "Pan-India mega-blockbusters agreement", 22.00, "Active", "2024-06-02 16:15:00"),
    (12, "CNT-2024-E4E-012", 12, "E4 South Indie Film Festival Winners Licensing", "Non-Exclusive Licensing", "2024-06-15", "2025-06-14", "India", "Award-winning Malayalam cinema license", 12.50, "Active", "2024-06-18 09:30:00"),
    (13, "CNT-2024-IND-013", 1, "Dharma Youth & College Rom-Com Package", "Non-Exclusive Licensing", "2024-07-01", "2025-12-31", "India", "Romantic comedy streaming catalog", 14.50, "Active", "2024-07-02 13:00:00"),
    (14, "CNT-2024-DOC-014", 4, "Excel Wildlife & Cultural Documentary Series", "Revenue Share", "2024-08-01", "2026-07-31", "Global", "Documentary revenue share arrangement", 18.00, "Active", "2024-08-05 11:20:00"),
    (15, "CNT-2024-EXP-015", 3, "T-Series Promotional Short Tracks Agreement", "Revenue Share", "2024-01-01", "2024-06-30", "India", "Expired promotional short licensing deal", 10.00, "Expired", "2024-01-02 10:00:00")
]

# 15. CONTRACT ASSETS (60 rows)
contract_assets_data = []
ca_id = 1
for a in assets_data[:58]:
    cid = ((a[0] - 1) % 14) + 1
    contract_assets_data.append((ca_id, cid, a[0], True, 100.00))
    ca_id += 1

# 16. SALES TRANSACTIONS (80 rows)
sales_data = []
st_id = 1
base_date = datetime(2024, 1, 15)
for i in range(1, 81):
    c_id = random.randint(1, 14)
    a_id = random.randint(1, 55)
    tx_code = f"TXN-2024-{i:04d}-{random.randint(100,999)}"
    units = random.randint(500, 25000)
    gross = round(units * random.uniform(2.5, 12.0), 2)
    platform_fee = round(gross * 0.15, 2)
    net = round(gross - platform_fee, 2)
    tx_date = (base_date + timedelta(days=i*4)).strftime("%Y-%m-%d")
    platform = random.choice(["MediaMerge OTT", "MediaMerge Mobile App", "Syndication Hub SAARC", "Tata Play Binge Partner"])
    territory = random.choice(["India", "India", "India", "SAARC", "Middle East"])
    sales_data.append((st_id, tx_code, c_id, a_id, platform, territory, units, gross, platform_fee, net, tx_date, f"{tx_date} 18:00:00"))
    st_id += 1

# 17. ROYALTY CALCULATIONS (55 rows)
calc_data = []
calc_id = 1
for i in range(1, 56):
    code = f"RC-2024-Q{((i%4)+1)}-{i:03d}"
    c_id = ((i - 1) % 14) + 1
    rh_id = contracts_data[c_id-1][2]
    rate = contracts_data[c_id-1][9]
    gross = round(random.uniform(150000.00, 2500000.00), 2)
    calculated = round(gross * (float(rate) / 100.0), 2)
    tax = round(calculated * 0.10, 2) # 10% TDS under Indian Income Tax Act
    net = round(calculated - tax, 2)
    status = "Paid" if i <= 35 else ("Approved" if i <= 48 else "Calculated")
    p_start = f"2024-{(i%10)+1:02d}-01"
    p_end = f"2024-{(i%10)+1:02d}-28"
    calc_data.append((calc_id, code, c_id, rh_id, p_start, p_end, gross, rate, calculated, tax, net, status, f"{p_end} 23:59:59"))
    calc_id += 1

# 18. ROYALTY PAYOUTS (35 rows - matching "Paid" calculations)
payouts_data = []
po_id = 1
for i in range(1, 36):
    calc_item = calc_data[i-1]
    ref = f"CMS-NEFT-IN{20240000 + i}{random.randint(10,99)}"
    mode = random.choice(["NEFT", "RTGS", "Direct Bank Transfer"])
    month = (i % 10) + 1
    tx_date = f"2024-{month:02d}-28"
    amount = calc_item[10]
    remarks = f"Quarterly royalty settlement for {contracts_data[calc_item[2]-1][1]} less TDS"
    payouts_data.append((po_id, calc_item[0], ref, mode, tx_date, amount, "Completed", remarks, f"{tx_date} 14:00:00"))
    po_id += 1

# 19. USER SUBSCRIPTIONS (60 rows)
user_subs_data = []
us_id = 1
for u in users_data:
    uid = u[0]
    plan_id = random.choice([2, 3, 4, 5])
    start = f"2024-03-{random.randint(1,25):02d}"
    end = "2025-03-31" if plan_id == 5 else f"2024-04-{random.randint(1,25):02d}"
    method = random.choice(["UPI (GPay / PhonePe)", "HDFC Credit Card", "ICICI Net Banking", "Paytm Wallet"])
    user_subs_data.append((us_id, uid, plan_id, start, end, "Active", True, method, f"{start} 10:00:00"))
    us_id += 1
# Extra subscriptions for history
for i in range(1, 44):
    uid = random.randint(9, 17)
    plan_id = random.choice([1, 2, 3, 4])
    start = f"2024-01-{random.randint(1,28):02d}"
    end = f"2024-02-{random.randint(1,28):02d}"
    status = "Expired"
    user_subs_data.append((us_id, uid, plan_id, start, end, status, False, "UPI", f"{start} 11:00:00"))
    us_id += 1

# 20. BILLING INVOICES (65 rows)
invoices_data = []
inv_id = 1
for sub in user_subs_data[:65]:
    inv_num = f"INV-2024-{inv_id:05d}"
    sid = sub[0]
    uid = sub[1]
    pid = sub[2]
    price = plans_data[pid-1][3]
    if price == 0:
        base = 0.00
        gst = 0.00
        total = 0.00
    else:
        base = round(float(price) / 1.18, 2)
        gst = round(float(price) - base, 2)
        total = float(price)
    inv_date = sub[3]
    paid_date = sub[3] if price > 0 else None
    invoices_data.append((inv_id, inv_num, sid, uid, base, 18.00, gst, total, "Paid", inv_date, paid_date, f"{inv_date} 10:05:00"))
    inv_id += 1

# 21. STREAMING SESSIONS (75 rows)
sessions_data = []
sess_id = 1
for i in range(1, 76):
    uid = random.randint(1, 17)
    aid = random.randint(1, 55)
    token = f"sess_{random.randint(10000000, 99999999)}_{i}"
    duration = random.randint(300, 7200)
    total_dur = assets_data[aid-1][7]
    pct = min(100.0, round((duration / max(total_dur, 1)) * 100.0, 2))
    quality = random.choice(["4K UHD", "1080p FHD", "720p HD", "Auto (1080p)"])
    device = random.choice(["Smart TV (Android TV)", "Apple TV 4K", "Chrome Web Player", "Mobile App (Android)", "iPad Air Safari"])
    ip = f"103.{random.randint(10,90)}.{random.randint(1,250)}.{random.randint(1,250)}"
    st_time = f"2024-{random.randint(4,10):02d}-{random.randint(1,28):02d} {random.randint(10,23):02d}:{random.randint(10,59):02d}:00"
    end_time = f"{st_time[:10]} 23:59:00"
    sessions_data.append((sess_id, token, uid, aid, st_time, end_time, duration, quality, device, ip, pct))
    sess_id += 1

# 22. DRM TOKENS (75 rows)
drm_tokens_data = []
dt_id = 1
for s in sessions_data:
    token_str = f"DRM_TOKEN_IN_{s[1]}_{random.randint(1000,9999)}"
    sid = s[0]
    uid = s[2]
    aid = s[3]
    iss = s[4]
    exp = f"{s[4][:10]} 23:59:59"
    lic = random.choice(["StreamingPlayback", "StreamingPlayback", "OfflineRental"])
    drm_tokens_data.append((dt_id, token_str, sid, uid, aid, iss, exp, lic, False))
    dt_id += 1

# 23. USER WATCH HISTORY (70 rows)
watch_history_data = []
wh_id = 1
seen_pairs = set()
for s in sessions_data:
    uid = s[2]
    aid = s[3]
    if (uid, aid) not in seen_pairs:
        seen_pairs.add((uid, aid))
        pos = s[6]
        tot = assets_data[aid-1][7]
        comp = pos >= (tot * 0.9)
        watch_history_data.append((wh_id, uid, aid, pos, tot, comp, s[4]))
        wh_id += 1

# 24. USER RATINGS & REVIEWS (55 rows)
reviews_data = []
r_id = 1
seen_revs = set()
comments_pool = [
    "Phenomenal cinematography and outstanding performance! Highly recommended.",
    "Masterpiece of Indian cinema. The audio mix and color grading are breathtaking.",
    "Riveting screenplay, loved the background score and intense narrative arc.",
    "Good watch with family, heartfelt storytelling and crisp editing.",
    "Visually stunning 4K restoration. Kudos to the preservation team!",
    "Engaging episodes throughout, keeps you hooked until the season finale.",
    "Soulful musical composition, listening to this on loop!",
    "Great direction and authentic portrayal of culture and heritage."
]
for i in range(1, 100):
    uid = random.randint(1, 17)
    aid = random.randint(1, 55)
    if (uid, aid) not in seen_revs:
        seen_revs.add((uid, aid))
        rating = random.choice([4, 5, 5, 4, 3, 5])
        review = random.choice(comments_pool)
        dt = f"2024-{random.randint(4,10):02d}-{random.randint(1,28):02d} 20:00:00"
        reviews_data.append((r_id, uid, aid, rating, review, dt))
        r_id += 1
        if len(reviews_data) >= 55:
            break

# 25. RECOMMENDATIONS (65 rows)
recs_data = []
rec_id = 1
seen_recs = set()
for uid in range(1, 18):
    for aid in random.sample(range(1, 56), 4):
        if (uid, aid) not in seen_recs:
            seen_recs.add((uid, aid))
            score = round(random.uniform(0.780, 0.995), 3)
            algo = random.choice(["CollaborativeFiltering+GenreMatch", "DeepContentSimilarity-Embeddings", "TrendingRegionalPopularity"])
            gen_at = f"2024-10-15 {random.randint(10,22):02d}:00:00"
            recs_data.append((rec_id, uid, aid, score, algo, gen_at))
            rec_id += 1

print(f"Data generation summary:")
print(f"Roles: {len(roles_data)}, Users: {len(users_data)}, Categories: {len(categories_data)}, Formats: {len(formats_data)}")
print(f"DRM Policies: {len(drm_data)}, Rights Holders: {len(rights_holders_data)}, Plans: {len(plans_data)}, Tags: {len(tags_data)}")
print(f"Assets: {len(assets_data)}, Metadata: {len(metadata_data)}, Versions: {len(versions_data)}, Perms: {len(perm_data)}")
print(f"Contracts: {len(contracts_data)}, Sales: {len(sales_data)}, Royalties: {len(calc_data)}, Payouts: {len(payouts_data)}")
print(f"Subscriptions: {len(user_subs_data)}, Invoices: {len(invoices_data)}, Sessions: {len(sessions_data)}, DRM Tokens: {len(drm_tokens_data)}")
print(f"Watch History: {len(watch_history_data)}, Reviews: {len(reviews_data)}, Recommendations: {len(recs_data)}")

# Write to CSV files
tables_map = {
    "roles.csv": (["role_id", "role_name", "description"], roles_data),
    "users.csv": (["user_id", "role_id", "full_name", "email", "password_hash", "phone_number", "city", "state", "is_active", "created_at"], users_data),
    "media_categories.csv": (["category_id", "category_name", "code", "description", "is_active"], categories_data),
    "media_formats.csv": (["format_id", "format_name", "resolution", "video_codec", "audio_codec", "container", "is_active"], formats_data),
    "drm_policies.csv": (["policy_id", "policy_name", "encryption_type", "allow_offline", "token_ttl_minutes", "watermark_enabled", "geo_restriction"], drm_data),
    "rights_holders.csv": (["rights_holder_id", "legal_name", "trade_name", "contact_person", "email", "phone", "city", "state", "gst_number", "pan_number"], rights_holders_data),
    "subscription_plans.csv": (["plan_id", "plan_name", "plan_tier", "price_inr", "billing_cycle_days", "max_screens", "video_quality", "is_active"], plans_data),
    "tags.csv": (["tag_id", "tag_name", "slug"], tags_data),
    "media_assets.csv": (["asset_id", "title", "description", "category_id", "format_id", "drm_policy_id", "rights_holder_id", "duration_seconds", "file_size_mb", "storage_path", "thumbnail_url", "censor_rating", "release_year", "primary_language", "status", "created_by", "created_at"], assets_data),
    "asset_metadata.csv": (["metadata_id", "asset_id", "meta_key", "meta_value", "data_type", "created_at"], metadata_data),
    "asset_tags.csv": (["asset_id", "tag_id"], asset_tags_data),
    "asset_versions.csv": (["version_id", "asset_id", "version_number", "file_path", "file_size_mb", "checksum_sha256", "change_summary", "created_by", "is_active", "created_at"], versions_data),
    "asset_permissions.csv": (["permission_id", "asset_id", "user_id", "role_id", "permission_type", "granted_by", "granted_at"], perm_data),
    "contracts.csv": (["contract_id", "contract_code", "rights_holder_id", "contract_title", "contract_type", "start_date", "end_date", "territory", "terms_summary", "royalty_rate_percent", "status", "signed_at"], contracts_data),
    "contract_assets.csv": (["contract_asset_id", "contract_id", "asset_id", "exclusivity", "royalty_split_percent"], contract_assets_data),
    "sales_transactions.csv": (["transaction_id", "transaction_code", "contract_id", "asset_id", "platform_name", "territory", "units_streamed", "gross_revenue_inr", "platform_fee_inr", "net_revenue_inr", "transaction_date", "created_at"], sales_data),
    "royalty_calculations.csv": (["calculation_id", "calculation_code", "contract_id", "rights_holder_id", "period_start", "period_end", "gross_sales_inr", "royalty_rate_percent", "calculated_royalty_inr", "tax_deduction_inr", "net_payable_inr", "payment_status", "processed_at"], calc_data),
    "royalty_payouts.csv": (["payout_id", "calculation_id", "payout_reference", "payment_mode", "transaction_date", "amount_inr", "status", "remarks", "created_at"], payouts_data),
    "user_subscriptions.csv": (["subscription_id", "user_id", "plan_id", "start_date", "end_date", "status", "auto_renew", "payment_method", "created_at"], user_subs_data),
    "billing_invoices.csv": (["invoice_id", "invoice_number", "subscription_id", "user_id", "base_amount_inr", "gst_rate_percent", "gst_amount_inr", "total_amount_inr", "payment_status", "invoice_date", "paid_date", "created_at"], invoices_data),
    "streaming_sessions.csv": (["session_id", "session_token", "user_id", "asset_id", "start_time", "end_time", "watch_duration_seconds", "playback_quality", "device_type", "ip_address", "completion_percentage"], sessions_data),
    "drm_tokens.csv": (["drm_token_id", "token_string", "session_id", "user_id", "asset_id", "issued_at", "expires_at", "license_type", "is_revoked"], drm_tokens_data),
    "user_watch_history.csv": (["history_id", "user_id", "asset_id", "last_playback_position_seconds", "total_duration_seconds", "completed", "updated_at"], watch_history_data),
    "user_ratings_reviews.csv": (["review_id", "user_id", "asset_id", "rating", "review_text", "created_at"], reviews_data),
    "recommendations.csv": (["recommendation_id", "user_id", "asset_id", "score", "recommendation_algorithm", "generated_at"], recs_data)
}

for fname, (headers, rows) in tables_map.items():
    fpath = os.path.join(CSV_DIR, fname)
    with open(fpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

print(f"Exported all {len(tables_map)} tables to CSV in {CSV_DIR}")

# Now generate seed_data.sql
def sql_val(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    v_escaped = str(v).replace("\\", "\\\\").replace("'", "''")
    return f"'{v_escaped}'"

with open(SQL_FILE, "w", encoding="utf-8") as sql_out:
    sql_out.write("-- =====================================================================\n")
    sql_out.write("-- MediaMerge - Realistic Indian Sample & Seed Data\n")
    sql_out.write("-- Target: MySQL 8.0+ | utf8mb4\n")
    sql_out.write("-- Parent tables are inserted before child tables to preserve FK integrity\n")
    sql_out.write("-- =====================================================================\n\n")
    sql_out.write("USE mediamerge_db;\n\n")
    sql_out.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

    for fname, (headers, rows) in tables_map.items():
        tbl_name = fname.replace(".csv", "")
        cols = ", ".join(f"`{h}`" for h in headers)
        sql_out.write(f"-- ---------------------------------------------------------------------\n")
        sql_out.write(f"-- TABLE: {tbl_name} ({len(rows)} rows)\n")
        sql_out.write(f"-- ---------------------------------------------------------------------\n")
        sql_out.write(f"INSERT INTO `{tbl_name}` ({cols}) VALUES\n")
        row_strs = []
        for r in rows:
            val_list = [sql_val(x) for x in r]
            row_strs.append("  (" + ", ".join(val_list) + ")")
        sql_out.write(",\n".join(row_strs) + ";\n\n")

    sql_out.write("SET FOREIGN_KEY_CHECKS = 1;\n")
    sql_out.write("-- End of Seed Data\n")

print(f"Generated complete seed_data.sql ({os.path.getsize(SQL_FILE)} bytes) at {SQL_FILE}")

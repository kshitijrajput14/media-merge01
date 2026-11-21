"""
Management command: enhance_database
Performs comprehensive database enhancements:
  1.  Adds 5 new users (diverse roles, cities)
  2.  Adds 3 new subscription plans (Freemium, Student, Enterprise)
  3.  Adds 10 new media assets (diverse genres, languages)
  4.  Adds 20 new sales transactions (Nov 2026) + royalty calculations
  5.  Adds 15 new watch-history records
  6.  Adds 10 new reviews with star ratings
  7.  Adds 20 new personalized recommendations
  8.  Creates 5 new contracts with asset links
  9.  Fixes NULL / inconsistent fields across all tables
  10. Prints a full analytics report
"""

from django.core.management.base import BaseCommand
from django.db.models import Avg, Sum, Count, Q
from decimal import Decimal
import random
import uuid
from datetime import date, timedelta

from core.models import Role, UserProfile
from assets.models import (
    MediaCategory, MediaFormat, Tag, MediaAsset,
    AssetMetadata, AssetTag, AssetVersion, AssetPermission
)
from rights.models import (
    RightsHolder, Contract, ContractAsset,
    SalesTransaction, RoyaltyCalculation, RoyaltyPayout
)
from streaming.models import DRMPolicy, StreamingSession, DRMToken
from subscriptions.models import SubscriptionPlan, UserSubscription, BillingInvoice
from analytics.models import UserWatchHistory, UserRatingReview, Recommendation


class Command(BaseCommand):
    help = 'Enhance database with new data, recalculations, and analytics'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*62))
        self.stdout.write(self.style.SUCCESS('  MediaMerge — Database Enhancement Script'))
        self.stdout.write(self.style.SUCCESS('='*62))

        self.add_new_users()
        self.add_new_subscription_plans()
        self.add_new_assets()
        self.add_new_sales_and_royalties()
        self.add_new_watch_history_and_reviews()
        self.add_new_recommendations()
        self.add_new_contracts()
        self.fix_null_fields()
        self.print_analytics_report()

        self.stdout.write(self.style.SUCCESS('\n✅  Database enhancement complete!\n'))

    # ------------------------------------------------------------------
    # 1. NEW USERS
    # ------------------------------------------------------------------
    def add_new_users(self):
        self.stdout.write('\n[1/9] Adding new users...')
        producer_role, _ = Role.objects.get_or_create(role_name='Producer')
        manager_role,  _ = Role.objects.get_or_create(role_name='Content Manager')
        viewer_role,   _ = Role.objects.get_or_create(role_name='Viewer')

        new_users = [
            dict(full_name='Priya Sharma',   email='priya.sharma@mediamerge.in',
                 phone_number='+91-9876543221', city='Jaipur',             state='Rajasthan',   role=producer_role),
            dict(full_name='Arjun Nair',     email='arjun.nair@mediamerge.in',
                 phone_number='+91-9123456781', city='Kochi',              state='Kerala',      role=manager_role),
            dict(full_name='Divya Pillai',   email='divya.pillai@mediamerge.in',
                 phone_number='+91-9988776655', city='Thiruvananthapuram', state='Kerala',      role=viewer_role),
            dict(full_name='Karan Mehta',    email='karan.mehta@mediamerge.in',
                 phone_number='+91-9871234560', city='Ahmedabad',          state='Gujarat',     role=viewer_role),
            dict(full_name='Sneha Iyer',     email='sneha.iyer@mediamerge.in',
                 phone_number='+91-9765432109', city='Chennai',            state='Tamil Nadu',  role=producer_role),
        ]
        created = 0
        for ud in new_users:
            if not UserProfile.objects.filter(email=ud['email']).exists():
                u = UserProfile(**ud)
                u.set_password('password123')
                u.is_active = True
                u.save()
                created += 1
        self.stdout.write(f'   ✓ Created {created} new users')

    # ------------------------------------------------------------------
    # 2. NEW SUBSCRIPTION PLANS
    # ------------------------------------------------------------------
    def add_new_subscription_plans(self):
        self.stdout.write('\n[2/9] Adding new subscription plans...')
        plans = [
            dict(plan_name='Freemium',   plan_tier='basic',    price_inr=Decimal('0'),
                 billing_cycle_days=30,  max_screens=1, video_quality='480p',   is_active=True),
            dict(plan_name='Student',    plan_tier='standard', price_inr=Decimal('99'),
                 billing_cycle_days=30,  max_screens=2, video_quality='720p',   is_active=True),
            dict(plan_name='Enterprise', plan_tier='premium',  price_inr=Decimal('2999'),
                 billing_cycle_days=365, max_screens=25, video_quality='4K',    is_active=True),
        ]
        created = 0
        for pd in plans:
            _, is_new = SubscriptionPlan.objects.get_or_create(plan_name=pd['plan_name'], defaults=pd)
            if is_new:
                created += 1
        self.stdout.write(f'   ✓ Created {created} new plans (Freemium, Student, Enterprise)')

    # ------------------------------------------------------------------
    # 3. NEW ASSETS
    # ------------------------------------------------------------------
    def add_new_assets(self):
        self.stdout.write('\n[3/9] Adding 10 new media assets...')
        cats         = list(MediaCategory.objects.all())
        fmts         = list(MediaFormat.objects.all())
        tags         = list(Tag.objects.all())
        holders      = list(RightsHolder.objects.all())
        drm_policies = list(DRMPolicy.objects.all())
        creator      = UserProfile.objects.first()

        new_assets = [
            ('Rang De Basanti Remastered',          'Hindi',   'Patriotic drama remaster in 4K HDR',           2026, 299, '4K',    'U/A 13+'),
            ('Chennai 600028 - Season 2',            'Tamil',   'Cricket comedy series sequel',                 2025, 149, '1080p', 'U'),
            ('Baahubali: The Lost Kingdom',          'Telugu',  'Fan-made prequel short film',                  2026,   0, '1080p', 'U/A 13+'),
            ('Arijit Singh Live - Mumbai 2026',      'Hindi',   'Full concert - Wankhede Stadium',              2026, 199, '4K',    'U'),
            ('Malgudi Days - Revival',               'Kannada', 'Modern adaptation of R.K. Narayan classic',   2025,  99, '1080p', 'U'),
            ('The Kashmir Files Documentary',        'Hindi',   'Behind-the-scenes documentary of the film',   2024,  49, '1080p', 'UA'),
            ('Ramayana Animated Series EP 1-26',     'Hindi',   'HD animated retelling for children',           2025, 199, '1080p', 'U'),
            ('Zakir Khan Haq Se Single 2',           'Hindi',   'Stand-up comedy special - Mumbai',             2026, 149, '4K',    'UA'),
            ('Tabla Maestro Masterclass',            'Hindi',   'Music learning series, 12 episodes',           2025, 349, '4K',    'U'),
            ('Sacred Geometry - Nature Documentary', 'English', 'Indian wildlife shot in 8K resolution',        2026, 299, '4K',    'U'),
        ]

        created = 0
        for i, (title, lang, desc, year, price, res, cbfc) in enumerate(new_assets):
            if not MediaAsset.objects.filter(title=title).exists():
                cat  = cats[i % len(cats)]   if cats         else None
                fmt  = fmts[i % len(fmts)]   if fmts         else None
                drm  = drm_policies[i % len(drm_policies)] if drm_policies else None
                rh   = holders[i % len(holders)]           if holders      else None

                dur_sec = random.randint(2700, 10800)   # 45 min – 3 hr in seconds
                size_mb = round(random.uniform(500, 8000), 2)

                asset = MediaAsset.objects.create(
                    title=title,
                    description=desc,
                    category=cat,
                    format=fmt,
                    primary_language=lang,
                    release_year=year,
                    duration_seconds=dur_sec,
                    file_size_mb=Decimal(str(size_mb)),
                    storage_path=f'/media/assets/{uuid.uuid4().hex[:8]}/{title.replace(" ", "_").lower()}.mp4',
                    thumbnail_url=f'https://cdn.mediamerge.in/thumbs/{uuid.uuid4().hex[:8]}.jpg',
                    censor_rating=cbfc,
                    status='published',
                    drm_policy=drm,
                    rights_holder=rh,
                    created_by=creator,
                )

                # 2 metadata entries
                AssetMetadata.objects.create(asset=asset, meta_key='genre',
                    meta_value=random.choice(['Drama', 'Comedy', 'Documentary', 'Music', 'Animation', 'Action']))
                AssetMetadata.objects.create(asset=asset, meta_key='resolution', meta_value=res)

                # 3 tags
                for tag in random.sample(tags, min(3, len(tags))):
                    AssetTag.objects.get_or_create(asset=asset, tag=tag)

                # Initial version
                AssetVersion.objects.create(
                    asset=asset,
                    version_number='1.0',
                    change_summary='Initial upload — Nov 2026 batch',
                    file_path=f'/media/assets/{asset.asset_id}/v1/{title.replace(" ", "_").lower()}.mp4',
                    file_size_mb=Decimal(str(size_mb)),
                    checksum_sha256=uuid.uuid4().hex,
                    is_active=True,
                    created_by=creator,
                )
                created += 1

        self.stdout.write(f'   ✓ Created {created} new assets')

    # ------------------------------------------------------------------
    # 4. NEW SALES + ROYALTY CALCULATIONS
    # ------------------------------------------------------------------
    def add_new_sales_and_royalties(self):
        self.stdout.write('\n[4/9] Adding 20 new sales transactions (Nov 2026) + royalties...')
        assets  = list(MediaAsset.objects.filter(status='published'))
        holders = list(RightsHolder.objects.all())
        contracts = list(Contract.objects.all())   # use all contracts, not just active

        platforms = ['JioCinema', 'Hotstar', 'SonyLIV', 'ZEE5', 'Amazon Prime Video',
                     'Netflix India', 'MX Player', 'Voot', 'Alt Balaji', 'Eros Now']
        territories = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi NCR', 'Telangana',
                       'West Bengal', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Kerala']

        if not contracts:
            self.stdout.write('   ⚠ No contracts found — skipping sales creation')
            return
        created_sales = 0
        if not contracts:
            self.stdout.write('   ⚠ No contracts found — skipping sales creation')
            return
        created_royalties = 0
        base_date = date(2026, 11, 1)

        for i in range(20):
            asset    = random.choice(assets)
            # contract is required (NOT NULL) — always pick one
            contract = contracts[i % len(contracts)] if contracts else None
            if contract is None:
                self.stdout.write('   ⚠ No contracts found, skipping sales creation')
                return
            gross    = Decimal(str(round(random.uniform(5000, 150000), 2)))
            fee      = (gross * Decimal('0.20')).quantize(Decimal('0.01'))
            net      = (gross - fee).quantize(Decimal('0.01'))
            units    = random.randint(50, 2000)
            txn_date = base_date + timedelta(days=random.randint(0, 19))

            sale = SalesTransaction.objects.create(
                transaction_code=f'TXN-NOV26-{uuid.uuid4().hex[:8].upper()}',
                contract=contract,
                asset=asset,
                platform_name=random.choice(platforms),
                territory=random.choice(territories),
                units_streamed=units,
                gross_revenue_inr=gross,
                platform_fee_inr=fee,
                net_revenue_inr=net,
                transaction_date=txn_date,
            )
            created_sales += 1

            # Royalty: 15% rate, 10% TDS (Section 194J)
            rate        = Decimal('15.00')
            holder      = random.choice(holders)
            calc_royalty = (gross * rate / 100).quantize(Decimal('0.01'))
            tds          = (calc_royalty * Decimal('0.10')).quantize(Decimal('0.01'))
            net_payable  = (calc_royalty - tds).quantize(Decimal('0.01'))

            RoyaltyCalculation.objects.create(
                calculation_code=f'RC-NOV26-{uuid.uuid4().hex[:8].upper()}',
                contract=contract,
                rights_holder=holder,
                period_start=base_date,
                period_end=base_date + timedelta(days=19),
                gross_sales_inr=gross,
                royalty_rate_percent=rate,
                calculated_royalty_inr=calc_royalty,
                tax_deduction_inr=tds,
                net_payable_inr=net_payable,
                payment_status='pending',
            )
            created_royalties += 1

        self.stdout.write(f'   ✓ Created {created_sales} sales transactions')
        self.stdout.write(f'   ✓ Created {created_royalties} royalty calculations')

    # ------------------------------------------------------------------
    # 5. WATCH HISTORY + REVIEWS
    # ------------------------------------------------------------------
    def add_new_watch_history_and_reviews(self):
        self.stdout.write('\n[5/9] Adding 15 watch history + 10 new reviews...')
        users  = list(UserProfile.objects.filter(is_active=True))
        assets = list(MediaAsset.objects.filter(status='published'))

        wh_created = 0
        for _ in range(15):
            user  = random.choice(users)
            asset = random.choice(assets)
            dur   = asset.duration_seconds or 5400
            watched = random.randint(300, dur)
            # update_or_create because (user, asset) is UNIQUE
            obj, created = UserWatchHistory.objects.update_or_create(
                user=user,
                asset=asset,
                defaults={
                    'last_playback_position_seconds': watched,
                    'total_duration_seconds': dur,
                    'completed': watched >= int(dur * 0.9),
                }
            )
            if created:
                wh_created += 1

        review_texts = [
            'अद्भुत फिल्म! पूरी तरह से सराहनीय। — Absolutely brilliant, highly recommend!',
            'Superb direction and cinematography. A must-watch for all cinema lovers.',
            'Average storyline but excellent music score. Worth watching once.',
            'Best Indian content I have seen in years. Proud of our creators!',
            'The 4K quality is stunning. Truly worth the subscription upgrade.',
            'Excellent performances. The climax was totally unexpected and gripping.',
            'Good content but needs better dubbing for regional languages.',
            'Binged all episodes in one night. Addictive storytelling!',
            'Beautifully shot. The Kerala backdrop adds so much depth.',
            'The documentary is an eye-opener. Every Indian should watch this.',
        ]
        rv_created = 0
        for i in range(10):
            user  = random.choice(users)
            asset = random.choice(assets)
            if not UserRatingReview.objects.filter(user=user, asset=asset).exists():
                UserRatingReview.objects.create(
                    user=user,
                    asset=asset,
                    rating=round(random.uniform(3.0, 5.0), 1),
                    review_text=review_texts[i],
                )
                rv_created += 1

        self.stdout.write(f'   ✓ Created {wh_created} watch history records')
        self.stdout.write(f'   ✓ Created {rv_created} new reviews')

    # ------------------------------------------------------------------
    # 6. NEW RECOMMENDATIONS
    # ------------------------------------------------------------------
    def add_new_recommendations(self):
        self.stdout.write('\n[6/9] Adding 20 personalized recommendations...')
        users  = list(UserProfile.objects.filter(is_active=True))
        assets = list(MediaAsset.objects.filter(status='published'))
        algos  = ['collaborative_filtering', 'content_based', 'trending', 'genre_based', 'hybrid']

        created = 0
        for _ in range(20):
            user  = random.choice(users)
            asset = random.choice(assets)
            if not Recommendation.objects.filter(user=user, asset=asset).exists():
                Recommendation.objects.create(
                    user=user,
                    asset=asset,
                    score=round(random.uniform(0.60, 0.99), 4),
                    recommendation_algorithm=random.choice(algos),
                )
                created += 1
        self.stdout.write(f'   ✓ Created {created} new recommendations')

    # ------------------------------------------------------------------
    # 7. NEW CONTRACTS
    # ------------------------------------------------------------------
    def add_new_contracts(self):
        self.stdout.write('\n[7/9] Adding 5 new contracts...')
        holders = list(RightsHolder.objects.all())
        assets  = list(MediaAsset.objects.filter(status='published'))
        ctypes  = ['Exclusive', 'Non-Exclusive', 'Co-Production', 'Distribution', 'Licensing']

        created = 0
        for i in range(5):
            holder = holders[i % len(holders)]
            code   = f'CTR-NOV26-{i+1:03d}'
            if not Contract.objects.filter(contract_code=code).exists():
                contract = Contract.objects.create(
                    contract_code=code,
                    rights_holder=holder,
                    contract_title=f'{ctypes[i]} Agreement {code}',
                    contract_type=ctypes[i],
                    start_date=date(2026, 11, 1),
                    end_date=date(2027, 10, 31),
                    territory='India',
                    terms_summary=f'Standard {ctypes[i].lower()} licensing terms for digital distribution across India.',
                    royalty_rate_percent=Decimal(str(round(random.uniform(10, 25), 2))),
                    status='active',
                    signed_at=date(2026, 10, 15),
                )
                for asset in random.sample(assets, min(2, len(assets))):
                    ContractAsset.objects.get_or_create(
                        contract=contract,
                        asset=asset,
                        defaults={
                            'exclusivity': i % 2 == 0,
                            'royalty_split_percent': Decimal(str(round(random.uniform(10, 50), 2)))
                        }
                    )
                created += 1

        self.stdout.write(f'   ✓ Created {created} new contracts with asset links')

    # ------------------------------------------------------------------
    # 8. FIX NULL / INCONSISTENT FIELDS
    # ------------------------------------------------------------------
    def fix_null_fields(self):
        self.stdout.write('\n[8/9] Fixing NULL fields and normalizing status values...')

        # Ensure all assets have a storage path
        fixed_path = 0
        for a in MediaAsset.objects.filter(storage_path__isnull=True):
            a.storage_path = f'/media/assets/{a.asset_id}/main.mp4'
            a.save(update_fields=['storage_path'])
            fixed_path += 1

        # Normalize royalty payment_status blanks → 'pending'
        fixed_royalty = RoyaltyCalculation.objects.filter(payment_status='').update(payment_status='pending')

        # Normalize subscription statuses
        fixed_subs = UserSubscription.objects.filter(
            status__in=['expired', 'EXPIRED']
        ).update(status='cancelled')

        # Set missing completion on watch history
        fixed_wh = 0
        for wh in UserWatchHistory.objects.filter(total_duration_seconds__gt=0):
            expected = wh.last_playback_position_seconds >= int(wh.total_duration_seconds * 0.9)
            if wh.completed != expected:
                wh.completed = expected
                wh.save(update_fields=['completed'])
                fixed_wh += 1

        self.stdout.write(f'   ✓ Fixed storage_path NULL   : {fixed_path} rows')
        self.stdout.write(f'   ✓ Fixed royalty status      : {fixed_royalty} rows')
        self.stdout.write(f'   ✓ Fixed subscription status : {fixed_subs} rows')
        self.stdout.write(f'   ✓ Fixed watch completion    : {fixed_wh} rows')

    # ------------------------------------------------------------------
    # 9. ANALYTICS REPORT
    # ------------------------------------------------------------------
    def print_analytics_report(self):
        self.stdout.write('\n[9/9] Running analytics queries...')
        self.stdout.write('\n' + '='*62)
        self.stdout.write('  📊  MEDIAMERGE — DATABASE ANALYTICS REPORT')
        self.stdout.write('='*62)

        # Inventory
        self.stdout.write('\n── INVENTORY ──────────────────────────────────────────────')
        self.stdout.write(f'  Total Users          : {UserProfile.objects.count()}')
        total_a   = MediaAsset.objects.count()
        pub_a     = MediaAsset.objects.filter(status='published').count()
        pend_a    = MediaAsset.objects.filter(status='pending').count()
        self.stdout.write(f'  Total Assets         : {total_a}  (Published: {pub_a}, Pending: {pend_a})')
        self.stdout.write(f'  Total Contracts      : {Contract.objects.count()} '
                          f'(Active: {Contract.objects.filter(status="active").count()})')
        self.stdout.write(f'  Total Subscriptions  : {UserSubscription.objects.count()} '
                          f'(Active: {UserSubscription.objects.filter(status="active").count()})')

        # Revenue
        self.stdout.write('\n── REVENUE ─────────────────────────────────────────────────')
        sales = SalesTransaction.objects.aggregate(total=Sum('gross_revenue_inr'), cnt=Count('transaction_id'))
        self.stdout.write(f'  Sales Transactions   : {sales["cnt"]}')
        self.stdout.write(f'  Gross Sales Revenue  : ₹{(sales["total"] or 0):,.2f}')

        roy = RoyaltyCalculation.objects.aggregate(
            calc=Sum('calculated_royalty_inr'),
            tds=Sum('tax_deduction_inr'),
            net=Sum('net_payable_inr'),
        )
        self.stdout.write(f'  Gross Royalties      : ₹{(roy["calc"] or 0):,.2f}')
        self.stdout.write(f'  TDS Deducted (194J)  : ₹{(roy["tds"]  or 0):,.2f}')
        self.stdout.write(f'  Net Payable           : ₹{(roy["net"]  or 0):,.2f}')

        inv = BillingInvoice.objects.aggregate(total=Sum('total_amount_inr'))
        self.stdout.write(f'  Total Billing Revenue: ₹{(inv["total"] or 0):,.2f}')

        # Top categories by asset count
        self.stdout.write('\n── TOP CATEGORIES BY ASSET COUNT ───────────────────────────')
        for c in MediaCategory.objects.annotate(ac=Count('assets')).order_by('-ac')[:5]:
            self.stdout.write(f'  {c.category_name:<30} : {c.ac} assets')

        # Top rated assets
        self.stdout.write('\n── TOP 5 RATED ASSETS ──────────────────────────────────────')
        for a in MediaAsset.objects.annotate(avg_r=Avg('reviews__rating')).filter(
            avg_r__isnull=False
        ).order_by('-avg_r')[:5]:
            self.stdout.write(f'  {a.title[:42]:<42} : ⭐ {a.avg_r:.2f}')

        # Subscription plan popularity
        self.stdout.write('\n── SUBSCRIPTION PLAN POPULARITY ────────────────────────────')
        for p in SubscriptionPlan.objects.annotate(subs=Count('subscriptions')).order_by('-subs'):
            self.stdout.write(f'  {p.plan_name:<20} : {p.subs:>3} subscribers | ₹{p.price_inr}/cycle')

        # Streaming analytics
        self.stdout.write('\n── STREAMING ANALYTICS ─────────────────────────────────────')
        wh = UserWatchHistory.objects.aggregate(
            total=Count('history_id'),
            completed=Count('history_id', filter=Q(completed=True)),
        )
        self.stdout.write(f'  Total Watch Sessions   : {wh["total"]}')
        self.stdout.write(f'  Completed Views        : {wh["completed"]}')
        self.stdout.write(f'  Streaming Sessions     : {StreamingSession.objects.count()}')
        self.stdout.write(f'  Active DRM Tokens      : {DRMToken.objects.count()}')

        # Recommendation engine
        self.stdout.write('\n── RECOMMENDATION ENGINE ────────────────────────────────────')
        total_rec = Recommendation.objects.count()
        self.stdout.write(f'  Total Recommendations  : {total_rec}')
        algo_counts = Recommendation.objects.values('recommendation_algorithm').annotate(
            cnt=Count('recommendation_id')
        ).order_by('-cnt')
        for ac in algo_counts:
            self.stdout.write(f'  {ac["recommendation_algorithm"]:<30} : {ac["cnt"]} recommendations')

        self.stdout.write('\n' + '='*62)

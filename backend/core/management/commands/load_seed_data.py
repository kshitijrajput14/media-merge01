import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Role, UserProfile
from assets.models import MediaCategory, MediaFormat, Tag, MediaAsset, AssetMetadata, AssetTag, AssetVersion, AssetPermission
from rights.models import RightsHolder, Contract, ContractAsset, SalesTransaction, RoyaltyCalculation, RoyaltyPayout
from streaming.models import DRMPolicy, StreamingSession, DRMToken
from subscriptions.models import SubscriptionPlan, UserSubscription, BillingInvoice
from analytics.models import UserWatchHistory, UserRatingReview, Recommendation

class Command(BaseCommand):
    help = "Loads seed data from CSV files into SQLite/MySQL database"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        csv_dir = os.path.join(base_dir, "database", "csv_data")

        if not os.path.exists(csv_dir):
            self.stdout.write(self.style.ERROR(f"CSV directory not found: {csv_dir}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Loading seed data from {csv_dir}..."))

        with transaction.atomic():
            # 1. Roles
            roles_map = {}
            with open(os.path.join(csv_dir, "roles.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = Role.objects.update_or_create(
                        role_id=int(r["role_id"]),
                        defaults={
                            "role_name": r["role_name"],
                            "description": r["description"] or None
                        }
                    )
                    roles_map[obj.role_id] = obj
            self.stdout.write(f"Loaded {len(roles_map)} roles")

            # 2. Users
            users_map = {}
            with open(os.path.join(csv_dir, "users.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = UserProfile.objects.update_or_create(
                        user_id=int(r["user_id"]),
                        defaults={
                            "role": roles_map[int(r["role_id"])],
                            "full_name": r["full_name"],
                            "email": r["email"],
                            "password_hash": r["password_hash"],
                            "phone_number": r["phone_number"] or None,
                            "city": r["city"] or None,
                            "state": r["state"] or None,
                            "is_active": r["is_active"] in ["True", "1", "true"]
                        }
                    )
                    users_map[obj.user_id] = obj
            self.stdout.write(f"Loaded {len(users_map)} users")

            # 3. Media Categories
            categories_map = {}
            with open(os.path.join(csv_dir, "media_categories.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = MediaCategory.objects.update_or_create(
                        category_id=int(r["category_id"]),
                        defaults={
                            "category_name": r["category_name"],
                            "code": r["code"],
                            "description": r["description"] or None,
                            "is_active": r["is_active"] in ["True", "1", "true"]
                        }
                    )
                    categories_map[obj.category_id] = obj
            self.stdout.write(f"Loaded {len(categories_map)} categories")

            # 4. Media Formats
            formats_map = {}
            with open(os.path.join(csv_dir, "media_formats.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = MediaFormat.objects.update_or_create(
                        format_id=int(r["format_id"]),
                        defaults={
                            "format_name": r["format_name"],
                            "resolution": r["resolution"],
                            "video_codec": r["video_codec"],
                            "audio_codec": r["audio_codec"],
                            "container": r["container"],
                            "is_active": r["is_active"] in ["True", "1", "true"]
                        }
                    )
                    formats_map[obj.format_id] = obj
            self.stdout.write(f"Loaded {len(formats_map)} formats")

            # 5. DRM Policies
            drm_map = {}
            with open(os.path.join(csv_dir, "drm_policies.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = DRMPolicy.objects.update_or_create(
                        policy_id=int(r["policy_id"]),
                        defaults={
                            "policy_name": r["policy_name"],
                            "encryption_type": r["encryption_type"],
                            "allow_offline": r["allow_offline"] in ["True", "1", "true"],
                            "token_ttl_minutes": int(r["token_ttl_minutes"]),
                            "watermark_enabled": r["watermark_enabled"] in ["True", "1", "true"],
                            "geo_restriction": r["geo_restriction"]
                        }
                    )
                    drm_map[obj.policy_id] = obj
            self.stdout.write(f"Loaded {len(drm_map)} DRM policies")

            # 6. Rights Holders
            rights_holders_map = {}
            with open(os.path.join(csv_dir, "rights_holders.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = RightsHolder.objects.update_or_create(
                        rights_holder_id=int(r["rights_holder_id"]),
                        defaults={
                            "legal_name": r["legal_name"],
                            "trade_name": r["trade_name"] or None,
                            "contact_person": r["contact_person"],
                            "email": r["email"],
                            "phone": r["phone"],
                            "city": r["city"],
                            "state": r["state"],
                            "gst_number": r["gst_number"] or None,
                            "pan_number": r["pan_number"] or None
                        }
                    )
                    rights_holders_map[obj.rights_holder_id] = obj
            self.stdout.write(f"Loaded {len(rights_holders_map)} rights holders")

            # 7. Subscription Plans
            plans_map = {}
            with open(os.path.join(csv_dir, "subscription_plans.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = SubscriptionPlan.objects.update_or_create(
                        plan_id=int(r["plan_id"]),
                        defaults={
                            "plan_name": r["plan_name"],
                            "plan_tier": r["plan_tier"],
                            "price_inr": float(r["price_inr"]),
                            "billing_cycle_days": int(r["billing_cycle_days"]),
                            "max_screens": int(r["max_screens"]),
                            "video_quality": r["video_quality"],
                            "is_active": r["is_active"] in ["True", "1", "true"]
                        }
                    )
                    plans_map[obj.plan_id] = obj
            self.stdout.write(f"Loaded {len(plans_map)} plans")

            # 8. Tags
            tags_map = {}
            with open(os.path.join(csv_dir, "tags.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    obj, _ = Tag.objects.update_or_create(
                        tag_id=int(r["tag_id"]),
                        defaults={
                            "tag_name": r["tag_name"],
                            "slug": r["slug"]
                        }
                    )
                    tags_map[obj.tag_id] = obj
            self.stdout.write(f"Loaded {len(tags_map)} tags")

            # 9. Media Assets
            assets_map = {}
            with open(os.path.join(csv_dir, "media_assets.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    creator = users_map.get(int(r["created_by"]), users_map[1])
                    obj, _ = MediaAsset.objects.update_or_create(
                        asset_id=int(r["asset_id"]),
                        defaults={
                            "title": r["title"],
                            "description": r["description"] or None,
                            "category": categories_map[int(r["category_id"])],
                            "format": formats_map[int(r["format_id"])],
                            "drm_policy": drm_map[int(r["drm_policy_id"])],
                            "rights_holder": rights_holders_map[int(r["rights_holder_id"])],
                            "duration_seconds": int(r["duration_seconds"]),
                            "file_size_mb": float(r["file_size_mb"]),
                            "storage_path": r["storage_path"],
                            "thumbnail_url": r["thumbnail_url"] or None,
                            "censor_rating": r["censor_rating"],
                            "release_year": int(r["release_year"]),
                            "primary_language": r["primary_language"],
                            "status": r["status"],
                            "created_by": creator
                        }
                    )
                    assets_map[obj.asset_id] = obj
            self.stdout.write(f"Loaded {len(assets_map)} assets")

            # 10. Asset Metadata
            meta_count = 0
            with open(os.path.join(csv_dir, "asset_metadata.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    aid = int(r["asset_id"])
                    if aid in assets_map:
                        AssetMetadata.objects.update_or_create(
                            metadata_id=int(r["metadata_id"]),
                            defaults={
                                "asset": assets_map[aid],
                                "meta_key": r["meta_key"],
                                "meta_value": r["meta_value"],
                                "data_type": r["data_type"]
                            }
                        )
                        meta_count += 1
            self.stdout.write(f"Loaded {meta_count} metadata entries")

            # 11. Asset Tags
            at_count = 0
            with open(os.path.join(csv_dir, "asset_tags.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    aid = int(r["asset_id"])
                    tid = int(r["tag_id"])
                    if aid in assets_map and tid in tags_map:
                        AssetTag.objects.get_or_create(
                            asset=assets_map[aid],
                            tag=tags_map[tid]
                        )
                        at_count += 1
            self.stdout.write(f"Loaded {at_count} asset tags")

            # 12. Asset Versions
            v_count = 0
            with open(os.path.join(csv_dir, "asset_versions.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    aid = int(r["asset_id"])
                    if aid in assets_map:
                        creator = users_map.get(int(r["created_by"]), users_map[1])
                        AssetVersion.objects.update_or_create(
                            version_id=int(r["version_id"]),
                            defaults={
                                "asset": assets_map[aid],
                                "version_number": r["version_number"],
                                "file_path": r["file_path"],
                                "file_size_mb": float(r["file_size_mb"]),
                                "checksum_sha256": r["checksum_sha256"],
                                "change_summary": r["change_summary"] or None,
                                "created_by": creator,
                                "is_active": r["is_active"] in ["True", "1", "true"]
                            }
                        )
                        v_count += 1
            self.stdout.write(f"Loaded {v_count} versions")

            # 13. Asset Permissions
            perm_count = 0
            with open(os.path.join(csv_dir, "asset_permissions.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    aid = int(r["asset_id"])
                    if aid in assets_map:
                        uid = int(r["user_id"]) if r["user_id"] else None
                        rid = int(r["role_id"]) if r["role_id"] else None
                        granter = users_map.get(int(r["granted_by"]), users_map[1])
                        AssetPermission.objects.update_or_create(
                            permission_id=int(r["permission_id"]),
                            defaults={
                                "asset": assets_map[aid],
                                "user": users_map.get(uid),
                                "role": roles_map.get(rid),
                                "permission_type": r["permission_type"],
                                "granted_by": granter
                            }
                        )
                        perm_count += 1
            self.stdout.write(f"Loaded {perm_count} asset permissions")

            # 14. Contracts
            contracts_map = {}
            with open(os.path.join(csv_dir, "contracts.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    rhid = int(r["rights_holder_id"])
                    obj, _ = Contract.objects.update_or_create(
                        contract_id=int(r["contract_id"]),
                        defaults={
                            "contract_code": r["contract_code"],
                            "rights_holder": rights_holders_map[rhid],
                            "contract_title": r["contract_title"],
                            "contract_type": r["contract_type"],
                            "start_date": r["start_date"],
                            "end_date": r["end_date"],
                            "territory": r["territory"],
                            "terms_summary": r["terms_summary"] or None,
                            "royalty_rate_percent": float(r["royalty_rate_percent"]),
                            "status": r["status"]
                        }
                    )
                    contracts_map[obj.contract_id] = obj
            self.stdout.write(f"Loaded {len(contracts_map)} contracts")

            # 15. Contract Assets
            ca_count = 0
            with open(os.path.join(csv_dir, "contract_assets.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cid = int(r["contract_id"])
                    aid = int(r["asset_id"])
                    if cid in contracts_map and aid in assets_map:
                        ContractAsset.objects.update_or_create(
                            contract_asset_id=int(r["contract_asset_id"]),
                            defaults={
                                "contract": contracts_map[cid],
                                "asset": assets_map[aid],
                                "exclusivity": r["exclusivity"] in ["True", "1", "true"],
                                "royalty_split_percent": float(r["royalty_split_percent"])
                            }
                        )
                        ca_count += 1
            self.stdout.write(f"Loaded {ca_count} contract assets")

            # 16. Sales Transactions
            st_count = 0
            with open(os.path.join(csv_dir, "sales_transactions.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cid = int(r["contract_id"])
                    aid = int(r["asset_id"])
                    if cid in contracts_map and aid in assets_map:
                        SalesTransaction.objects.update_or_create(
                            transaction_id=int(r["transaction_id"]),
                            defaults={
                                "transaction_code": r["transaction_code"],
                                "contract": contracts_map[cid],
                                "asset": assets_map[aid],
                                "platform_name": r["platform_name"],
                                "territory": r["territory"],
                                "units_streamed": int(r["units_streamed"]),
                                "gross_revenue_inr": float(r["gross_revenue_inr"]),
                                "platform_fee_inr": float(r["platform_fee_inr"]),
                                "net_revenue_inr": float(r["net_revenue_inr"]),
                                "transaction_date": r["transaction_date"]
                            }
                        )
                        st_count += 1
            self.stdout.write(f"Loaded {st_count} sales transactions")

            # 17. Royalty Calculations
            calcs_map = {}
            with open(os.path.join(csv_dir, "royalty_calculations.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cid = int(r["contract_id"])
                    rhid = int(r["rights_holder_id"])
                    if cid in contracts_map and rhid in rights_holders_map:
                        obj, _ = RoyaltyCalculation.objects.update_or_create(
                            calculation_id=int(r["calculation_id"]),
                            defaults={
                                "calculation_code": r["calculation_code"],
                                "contract": contracts_map[cid],
                                "rights_holder": rights_holders_map[rhid],
                                "period_start": r["period_start"],
                                "period_end": r["period_end"],
                                "gross_sales_inr": float(r["gross_sales_inr"]),
                                "royalty_rate_percent": float(r["royalty_rate_percent"]),
                                "calculated_royalty_inr": float(r["calculated_royalty_inr"]),
                                "tax_deduction_inr": float(r["tax_deduction_inr"]),
                                "net_payable_inr": float(r["net_payable_inr"]),
                                "payment_status": r["payment_status"]
                            }
                        )
                        calcs_map[obj.calculation_id] = obj
            self.stdout.write(f"Loaded {len(calcs_map)} royalty calculations")

            # 18. Royalty Payouts
            rp_count = 0
            with open(os.path.join(csv_dir, "royalty_payouts.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    calc_id = int(r["calculation_id"])
                    if calc_id in calcs_map:
                        RoyaltyPayout.objects.update_or_create(
                            payout_id=int(r["payout_id"]),
                            defaults={
                                "calculation": calcs_map[calc_id],
                                "payout_reference": r["payout_reference"],
                                "payment_mode": r["payment_mode"],
                                "transaction_date": r["transaction_date"],
                                "amount_inr": float(r["amount_inr"]),
                                "status": r["status"],
                                "remarks": r["remarks"] or None
                            }
                        )
                        rp_count += 1
            self.stdout.write(f"Loaded {rp_count} royalty payouts")

            # 19. User Subscriptions
            subs_map = {}
            with open(os.path.join(csv_dir, "user_subscriptions.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    uid = int(r["user_id"])
                    pid = int(r["plan_id"])
                    if uid in users_map and pid in plans_map:
                        obj, _ = UserSubscription.objects.update_or_create(
                            subscription_id=int(r["subscription_id"]),
                            defaults={
                                "user": users_map[uid],
                                "plan": plans_map[pid],
                                "start_date": r["start_date"],
                                "end_date": r["end_date"],
                                "status": r["status"],
                                "auto_renew": r["auto_renew"] in ["True", "1", "true"],
                                "payment_method": r["payment_method"]
                            }
                        )
                        subs_map[obj.subscription_id] = obj
            self.stdout.write(f"Loaded {len(subs_map)} subscriptions")

            # 20. Billing Invoices
            inv_count = 0
            with open(os.path.join(csv_dir, "billing_invoices.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sid = int(r["subscription_id"])
                    uid = int(r["user_id"])
                    if sid in subs_map and uid in users_map:
                        BillingInvoice.objects.update_or_create(
                            invoice_id=int(r["invoice_id"]),
                            defaults={
                                "invoice_number": r["invoice_number"],
                                "subscription": subs_map[sid],
                                "user": users_map[uid],
                                "base_amount_inr": float(r["base_amount_inr"]),
                                "gst_rate_percent": float(r["gst_rate_percent"]),
                                "gst_amount_inr": float(r["gst_amount_inr"]),
                                "total_amount_inr": float(r["total_amount_inr"]),
                                "payment_status": r["payment_status"],
                                "invoice_date": r["invoice_date"],
                                "paid_date": r["paid_date"] or None
                            }
                        )
                        inv_count += 1
            self.stdout.write(f"Loaded {inv_count} invoices")

            # 21. Streaming Sessions
            sessions_map = {}
            with open(os.path.join(csv_dir, "streaming_sessions.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    uid = int(r["user_id"])
                    aid = int(r["asset_id"])
                    if uid in users_map and aid in assets_map:
                        obj, _ = StreamingSession.objects.update_or_create(
                            session_id=int(r["session_id"]),
                            defaults={
                                "session_token": r["session_token"],
                                "user": users_map[uid],
                                "asset": assets_map[aid],
                                "watch_duration_seconds": int(r["watch_duration_seconds"]),
                                "playback_quality": r["playback_quality"],
                                "device_type": r["device_type"],
                                "ip_address": r["ip_address"],
                                "completion_percentage": float(r["completion_percentage"])
                            }
                        )
                        sessions_map[obj.session_id] = obj
            self.stdout.write(f"Loaded {len(sessions_map)} streaming sessions")

            # 22. DRM Tokens
            dt_count = 0
            with open(os.path.join(csv_dir, "drm_tokens.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sid = int(r["session_id"])
                    uid = int(r["user_id"])
                    aid = int(r["asset_id"])
                    if sid in sessions_map and uid in users_map and aid in assets_map:
                        DRMToken.objects.update_or_create(
                            drm_token_id=int(r["drm_token_id"]),
                            defaults={
                                "token_string": r["token_string"],
                                "session": sessions_map[sid],
                                "user": users_map[uid],
                                "asset": assets_map[aid],
                                "expires_at": r["expires_at"],
                                "license_type": r["license_type"],
                                "is_revoked": r["is_revoked"] in ["True", "1", "true"]
                            }
                        )
                        dt_count += 1
            self.stdout.write(f"Loaded {dt_count} DRM tokens")

            # 23. User Watch History
            wh_count = 0
            with open(os.path.join(csv_dir, "user_watch_history.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    uid = int(r["user_id"])
                    aid = int(r["asset_id"])
                    if uid in users_map and aid in assets_map:
                        UserWatchHistory.objects.update_or_create(
                            history_id=int(r["history_id"]),
                            defaults={
                                "user": users_map[uid],
                                "asset": assets_map[aid],
                                "last_playback_position_seconds": int(r["last_playback_position_seconds"]),
                                "total_duration_seconds": int(r["total_duration_seconds"]),
                                "completed": r["completed"] in ["True", "1", "true"]
                            }
                        )
                        wh_count += 1
            self.stdout.write(f"Loaded {wh_count} watch history records")

            # 24. User Ratings Reviews
            rev_count = 0
            with open(os.path.join(csv_dir, "user_ratings_reviews.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    uid = int(r["user_id"])
                    aid = int(r["asset_id"])
                    if uid in users_map and aid in assets_map:
                        UserRatingReview.objects.update_or_create(
                            review_id=int(r["review_id"]),
                            defaults={
                                "user": users_map[uid],
                                "asset": assets_map[aid],
                                "rating": int(r["rating"]),
                                "review_text": r["review_text"] or None
                            }
                        )
                        rev_count += 1
            self.stdout.write(f"Loaded {rev_count} ratings and reviews")

            # 25. Recommendations
            rec_count = 0
            with open(os.path.join(csv_dir, "recommendations.csv"), encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    uid = int(r["user_id"])
                    aid = int(r["asset_id"])
                    if uid in users_map and aid in assets_map:
                        Recommendation.objects.update_or_create(
                            recommendation_id=int(r["recommendation_id"]),
                            defaults={
                                "user": users_map[uid],
                                "asset": assets_map[aid],
                                "score": float(r["score"]),
                                "recommendation_algorithm": r["recommendation_algorithm"]
                            }
                        )
                        rec_count += 1
            self.stdout.write(f"Loaded {rec_count} recommendations")

        self.stdout.write(self.style.SUCCESS("All seed data successfully loaded into database!"))

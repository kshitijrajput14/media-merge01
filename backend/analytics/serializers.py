from rest_framework import serializers
from .models import UserWatchHistory, UserRatingReview, Recommendation
from assets.serializers import MediaAssetListSerializer

class UserWatchHistorySerializer(serializers.ModelSerializer):
    asset_title = serializers.CharField(source='asset.title', read_only=True)
    thumbnail_url = serializers.CharField(source='asset.thumbnail_url', read_only=True)

    class Meta:
        model = UserWatchHistory
        fields = '__all__'


class UserRatingReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = UserRatingReview
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    asset_details = MediaAssetListSerializer(source='asset', read_only=True)

    class Meta:
        model = Recommendation
        fields = '__all__'

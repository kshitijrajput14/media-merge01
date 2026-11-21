from rest_framework import serializers
from .models import MediaCategory, MediaFormat, Tag, MediaAsset, AssetMetadata, AssetVersion, AssetPermission
from core.serializers import UserProfileSerializer

class MediaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = '__all__'


class MediaFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFormat
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AssetMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMetadata
        fields = '__all__'


class AssetVersionSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='created_by.full_name', read_only=True)
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = AssetVersion
        fields = ['version_id', 'asset', 'asset_title', 'version_number', 'file_path', 'file_size_mb', 'checksum_sha256', 'change_summary', 'created_by', 'creator_name', 'is_active', 'created_at']


class AssetPermissionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    granter_name = serializers.CharField(source='granted_by.full_name', read_only=True)

    class Meta:
        model = AssetPermission
        fields = ['permission_id', 'asset', 'user', 'user_name', 'role', 'role_name', 'permission_type', 'granted_by', 'granter_name', 'granted_at']


class MediaAssetListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    format_name = serializers.CharField(source='format.format_name', read_only=True)
    rights_holder_name = serializers.CharField(source='rights_holder.legal_name', read_only=True)
    creator_name = serializers.CharField(source='created_by.full_name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MediaAsset
        fields = [
            'asset_id', 'title', 'description', 'category', 'category_name',
            'format', 'format_name', 'drm_policy', 'rights_holder', 'rights_holder_name',
            'duration_seconds', 'file_size_mb', 'storage_path', 'thumbnail_url',
            'censor_rating', 'release_year', 'primary_language', 'status',
            'created_by', 'creator_name', 'tags', 'created_at', 'updated_at'
        ]


class MediaAssetDetailSerializer(serializers.ModelSerializer):
    category_details = MediaCategorySerializer(source='category', read_only=True)
    format_details = MediaFormatSerializer(source='format', read_only=True)
    rights_holder_name = serializers.CharField(source='rights_holder.legal_name', read_only=True)
    creator_name = serializers.CharField(source='created_by.full_name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    metadata_entries = AssetMetadataSerializer(many=True, read_only=True)
    versions = AssetVersionSerializer(many=True, read_only=True)
    permissions = AssetPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = MediaAsset
        fields = '__all__'

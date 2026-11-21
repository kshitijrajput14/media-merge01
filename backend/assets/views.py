import hashlib
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import MediaCategory, MediaFormat, Tag, MediaAsset, AssetMetadata, AssetVersion, AssetPermission
from .serializers import (
    MediaCategorySerializer, MediaFormatSerializer, TagSerializer,
    MediaAssetListSerializer, MediaAssetDetailSerializer,
    AssetMetadataSerializer, AssetVersionSerializer, AssetPermissionSerializer
)

class MediaCategoryViewSet(viewsets.ModelViewSet):
    queryset = MediaCategory.objects.all()
    serializer_class = MediaCategorySerializer
    permission_classes = [AllowAny]


class MediaFormatViewSet(viewsets.ModelViewSet):
    queryset = MediaFormat.objects.all()
    serializer_class = MediaFormatSerializer
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class AssetVersionViewSet(viewsets.ModelViewSet):
    queryset = AssetVersion.objects.all().select_related('asset', 'created_by').order_by('-created_at')
    serializer_class = AssetVersionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        asset_id = self.request.query_params.get('asset_id')
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs


class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.all().select_related(
        'category', 'format', 'drm_policy', 'rights_holder', 'created_by'
    ).prefetch_related('tags')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MediaAssetDetailSerializer
        return MediaAssetListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        format_id = self.request.query_params.get('format')
        status_param = self.request.query_params.get('status')
        language = self.request.query_params.get('language')
        censor = self.request.query_params.get('censor')
        year = self.request.query_params.get('year')
        search = self.request.query_params.get('search')
        tag = self.request.query_params.get('tag')

        if category:
            qs = qs.filter(category_id=category)
        if format_id:
            qs = qs.filter(format_id=format_id)
        if status_param:
            qs = qs.filter(status__iexact=status_param)
        if language:
            qs = qs.filter(primary_language__iexact=language)
        if censor:
            qs = qs.filter(censor_rating=censor)
        if year:
            qs = qs.filter(release_year=year)
        if tag:
            qs = qs.filter(tags__slug=tag)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(primary_language__icontains=search) |
                Q(rights_holder__legal_name__icontains=search)
            ).distinct()

        return qs

    @action(detail=True, methods=['post'], url_path='versions')
    def add_version(self, request, pk=None):
        asset = self.get_object()
        version_num = request.data.get('version_number')
        file_path = request.data.get('file_path', f"{asset.storage_path}_v_new")
        file_size_mb = request.data.get('file_size_mb', asset.file_size_mb)
        change_summary = request.data.get('change_summary', 'Incremental asset revision')
        created_by_id = request.data.get('created_by', asset.created_by_id)
        is_active = request.data.get('is_active', False)

        if not version_num:
            existing_count = asset.versions.count()
            version_num = f"v1.{existing_count}.0"

        checksum = hashlib.sha256(f"{asset.title}_{version_num}_{file_path}".encode('utf-8')).hexdigest()

        if is_active:
            asset.versions.update(is_active=False)

        version = AssetVersion.objects.create(
            asset=asset,
            version_number=version_num,
            file_path=file_path,
            file_size_mb=file_size_mb,
            checksum_sha256=checksum,
            change_summary=change_summary,
            created_by_id=created_by_id,
            is_active=is_active
        )
        return Response(AssetVersionSerializer(version).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='rollback/(?P<version_id>[^/.]+)')
    def rollback_version(self, request, pk=None, version_id=None):
        asset = self.get_object()
        try:
            target_version = asset.versions.get(version_id=version_id)
        except AssetVersion.DoesNotExist:
            return Response({'error': 'Version not found for this asset'}, status=status.HTTP_404_NOT_FOUND)

        asset.versions.update(is_active=False)
        target_version.is_active = True
        target_version.save()

        asset.storage_path = target_version.file_path
        asset.file_size_mb = target_version.file_size_mb
        asset.save()

        return Response({
            'message': f"Asset successfully rolled back to version {target_version.version_number}",
            'active_version': AssetVersionSerializer(target_version).data
        })

    @action(detail=True, methods=['post'], url_path='permissions')
    def grant_permission(self, request, pk=None):
        asset = self.get_object()
        perm_type = request.data.get('permission_type', 'view')
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')
        granted_by_id = request.data.get('granted_by', 1)

        perm = AssetPermission.objects.create(
            asset=asset,
            user_id=user_id,
            role_id=role_id,
            permission_type=perm_type,
            granted_by_id=granted_by_id
        )
        return Response(AssetPermissionSerializer(perm).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='metadata')
    def add_or_update_metadata(self, request, pk=None):
        asset = self.get_object()
        meta_key = request.data.get('meta_key')
        meta_value = request.data.get('meta_value')
        data_type = request.data.get('data_type', 'string')

        if not meta_key or meta_value is None:
            return Response({'error': 'meta_key and meta_value are required'}, status=status.HTTP_400_BAD_REQUEST)

        meta, _ = AssetMetadata.objects.update_or_create(
            asset=asset,
            meta_key=meta_key,
            defaults={'meta_value': str(meta_value), 'data_type': data_type}
        )
        return Response(AssetMetadataSerializer(meta).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_and_retrieval_view(request):
    """Advanced faceted search across media assets, metadata, tags, and rights holders"""
    query = request.query_params.get('q', '').strip()
    category = request.query_params.get('category')
    format_type = request.query_params.get('format')
    language = request.query_params.get('language')
    censor = request.query_params.get('censor')
    year_from = request.query_params.get('year_from')
    year_to = request.query_params.get('year_to')
    min_duration = request.query_params.get('min_duration')
    max_duration = request.query_params.get('max_duration')
    sort_by = request.query_params.get('sort_by', '-asset_id')

    qs = MediaAsset.objects.all().select_related('category', 'format', 'rights_holder')

    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(metadata_entries__meta_value__icontains=query) |
            Q(tags__tag_name__icontains=query) |
            Q(rights_holder__legal_name__icontains=query)
        ).distinct()

    if category:
        qs = qs.filter(category__code__iexact=category) | qs.filter(category__category_name__icontains=category)
    if format_type:
        qs = qs.filter(format__format_name__icontains=format_type)
    if language:
        qs = qs.filter(primary_language__iexact=language)
    if censor:
        qs = qs.filter(censor_rating=censor)
    if year_from:
        qs = qs.filter(release_year__gte=int(year_from))
    if year_to:
        qs = qs.filter(release_year__lte=int(year_to))
    if min_duration:
        qs = qs.filter(duration_seconds__gte=int(min_duration))
    if max_duration:
        qs = qs.filter(duration_seconds__lte=int(max_duration))

    # Facet counts for filters
    facets = {
        'total_matches': qs.count(),
        'languages': list(qs.values_list('primary_language', flat=True).distinct()),
        'censor_ratings': list(qs.values_list('censor_rating', flat=True).distinct()),
        'categories': list(MediaCategory.objects.filter(is_active=True).values('category_id', 'category_name', 'code')),
    }

    if sort_by in ['title', '-title', 'release_year', '-release_year', 'duration_seconds', '-duration_seconds', '-asset_id']:
        qs = qs.order_by(sort_by)

    data = MediaAssetListSerializer(qs[:50], many=True).data
    return Response({
        'facets': facets,
        'results': data
    })

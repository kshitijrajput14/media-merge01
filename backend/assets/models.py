from django.db import models
from django.utils import timezone

class MediaCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'media_categories'
        ordering = ['category_id']

    def __str__(self):
        return self.category_name


class MediaFormat(models.Model):
    format_id = models.AutoField(primary_key=True)
    format_name = models.CharField(max_length=50, unique=True)
    resolution = models.CharField(max_length=30)
    video_codec = models.CharField(max_length=30)
    audio_codec = models.CharField(max_length=30)
    container = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'media_formats'
        ordering = ['format_id']

    def __str__(self):
        return self.format_name


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = 'tags'
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name


class MediaAsset(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Review', 'Review'),
        ('Approved', 'Approved'),
        ('Published', 'Published'),
        ('Archived', 'Archived'),
    ]

    asset_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(MediaCategory, on_delete=models.RESTRICT, related_name='assets')
    format = models.ForeignKey(MediaFormat, on_delete=models.RESTRICT, related_name='assets')
    drm_policy = models.ForeignKey('streaming.DRMPolicy', on_delete=models.RESTRICT, related_name='assets')
    rights_holder = models.ForeignKey('rights.RightsHolder', on_delete=models.RESTRICT, related_name='assets')
    duration_seconds = models.IntegerField(default=0)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    storage_path = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)
    censor_rating = models.CharField(max_length=10, default='U/A 13+')
    release_year = models.IntegerField(default=2024)
    primary_language = models.CharField(max_length=40, default='Hindi')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_by = models.ForeignKey('core.UserProfile', on_delete=models.RESTRICT, related_name='created_assets')
    tags = models.ManyToManyField(Tag, through='AssetTag', related_name='assets')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_assets'
        ordering = ['-asset_id']

    def __str__(self):
        return f"{self.title} ({self.release_year}) - [{self.status}]"


class AssetMetadata(models.Model):
    DATA_TYPES = [
        ('string', 'string'),
        ('number', 'number'),
        ('boolean', 'boolean'),
        ('json', 'json'),
    ]

    metadata_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='metadata_entries')
    meta_key = models.CharField(max_length=80)
    meta_value = models.TextField()
    data_type = models.CharField(max_length=20, choices=DATA_TYPES, default='string')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_metadata'
        unique_together = ('asset', 'meta_key')

    def __str__(self):
        return f"{self.asset.title} -> {self.meta_key}: {self.meta_value[:30]}"


class AssetTag(models.Model):
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'asset_tags'
        unique_together = ('asset', 'tag')


class AssetVersion(models.Model):
    version_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20)
    file_path = models.CharField(max_length=255)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2)
    checksum_sha256 = models.CharField(max_length=64)
    change_summary = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey('core.UserProfile', on_delete=models.RESTRICT, related_name='created_versions')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_versions'
        unique_together = ('asset', 'version_number')
        ordering = ['-version_id']

    def __str__(self):
        return f"{self.asset.title} ({self.version_number})"


class AssetPermission(models.Model):
    PERMISSION_TYPES = [
        ('view', 'view'),
        ('edit', 'edit'),
        ('download', 'download'),
        ('publish', 'publish'),
        ('delete', 'delete'),
    ]

    permission_id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='asset_permissions')
    role = models.ForeignKey('core.Role', on_delete=models.CASCADE, null=True, blank=True, related_name='role_asset_permissions')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    granted_by = models.ForeignKey('core.UserProfile', on_delete=models.RESTRICT, related_name='granted_permissions')
    granted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'asset_permissions'

    def __str__(self):
        target = self.user.full_name if self.user else f"Role: {self.role.role_name}"
        return f"Asset #{self.asset_id} -> {self.permission_type} ({target})"

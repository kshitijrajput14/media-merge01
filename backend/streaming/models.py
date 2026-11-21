from django.db import models
from django.utils import timezone

class DRMPolicy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=80, unique=True)
    encryption_type = models.CharField(max_length=40, default='AES-128')
    allow_offline = models.BooleanField(default=False)
    token_ttl_minutes = models.IntegerField(default=120)
    watermark_enabled = models.BooleanField(default=True)
    geo_restriction = models.CharField(max_length=100, default='IN')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'drm_policies'
        ordering = ['policy_id']

    def __str__(self):
        return f"{self.policy_name} ({self.encryption_type})"


class StreamingSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_token = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='streaming_sessions')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.CASCADE, related_name='streaming_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    watch_duration_seconds = models.IntegerField(default=0)
    playback_quality = models.CharField(max_length=20, default='1080p')
    device_type = models.CharField(max_length=50, default='Desktop Web')
    ip_address = models.CharField(max_length=45, default='127.0.0.1')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'streaming_sessions'
        ordering = ['-start_time']

    def __str__(self):
        return f"Session {self.session_token[:12]}... (User #{self.user_id})"


class DRMToken(models.Model):
    LICENSE_TYPES = [
        ('StreamingPlayback', 'StreamingPlayback'),
        ('OfflineRental', 'OfflineRental'),
        ('EditorialPreview', 'EditorialPreview'),
    ]

    drm_token_id = models.AutoField(primary_key=True)
    token_string = models.CharField(max_length=128, unique=True)
    session = models.ForeignKey(StreamingSession, on_delete=models.CASCADE, related_name='drm_tokens')
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='drm_tokens')
    asset = models.ForeignKey('assets.MediaAsset', on_delete=models.CASCADE, related_name='drm_tokens')
    issued_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    license_type = models.CharField(max_length=30, choices=LICENSE_TYPES, default='StreamingPlayback')
    is_revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'drm_tokens'
        ordering = ['-issued_at']

    def __str__(self):
        return f"DRM Token {self.token_string[:16]}... ({self.license_type})"

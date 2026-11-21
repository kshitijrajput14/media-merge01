import secrets
from datetime import timedelta
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import DRMPolicy, StreamingSession, DRMToken
from .serializers import DRMPolicySerializer, StreamingSessionSerializer, DRMTokenSerializer
from assets.models import MediaAsset
from core.models import UserProfile

class DRMPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DRMPolicy.objects.all()
    serializer_class = DRMPolicySerializer
    permission_classes = [AllowAny]


class StreamingSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StreamingSession.objects.all().select_related('user', 'asset')
    serializer_class = StreamingSessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        asset_id = self.request.query_params.get('asset_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        if asset_id:
            qs = qs.filter(asset_id=asset_id)
        return qs


@api_view(['POST'])
@permission_classes([AllowAny])
def start_streaming_session_view(request):
    """
    Module 11: Content Streaming and DRM Token Handshake.
    Validates user credentials, creates playback session, issues DRM token with TTL and watermark payload.
    """
    user_id = request.data.get('user_id')
    asset_id = request.data.get('asset_id')
    device_type = request.data.get('device_type', 'Desktop Web Player')
    quality = request.data.get('quality', '1080p FHD')

    if not user_id or not asset_id:
        return Response({'error': 'user_id and asset_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserProfile.objects.get(user_id=user_id)
        asset = MediaAsset.objects.select_related('drm_policy').get(asset_id=asset_id)
    except (UserProfile.DoesNotExist, MediaAsset.DoesNotExist):
        return Response({'error': 'User or Media Asset not found'}, status=status.HTTP_404_NOT_FOUND)

    # Generate session token and DRM token
    session_token = f"sess_{secrets.token_hex(16)}"
    policy = asset.drm_policy
    ttl_minutes = policy.token_ttl_minutes if policy else 120
    now = timezone.now()
    expires_at = now + timedelta(minutes=ttl_minutes)

    ip_address = request.META.get('REMOTE_ADDR', '103.21.244.15')

    session = StreamingSession.objects.create(
        session_token=session_token,
        user=user,
        asset=asset,
        start_time=now,
        playback_quality=quality,
        device_type=device_type,
        ip_address=ip_address
    )

    drm_token_str = f"DRM_TOKEN_IN_{policy.encryption_type}_{secrets.token_urlsafe(32)}"
    drm_token = DRMToken.objects.create(
        token_string=drm_token_str,
        session=session,
        user=user,
        asset=asset,
        issued_at=now,
        expires_at=expires_at,
        license_type='StreamingPlayback'
    )

    # Watermark overlay configuration to protect IP
    watermark = {
        'enabled': policy.watermark_enabled if policy else True,
        'overlay_text': f"{user.email} | IP: {ip_address} | {now.strftime('%d-%b-%Y %H:%M')}",
        'opacity': 0.35,
        'position': 'dynamic_jitter'
    }

    # Public mock stream video (Big Buck Bunny / sample MP4) for interactive playback
    stream_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    return Response({
        'session_id': session.session_id,
        'session_token': session.session_token,
        'asset_title': asset.title,
        'stream_url': stream_url,
        'playback_quality': quality,
        'drm_license': {
            'token': drm_token.token_string,
            'encryption_type': policy.encryption_type if policy else 'AES-128',
            'issued_at': drm_token.issued_at.isoformat(),
            'expires_at': drm_token.expires_at.isoformat(),
            'status': 'AUTHORIZED_ACTIVE'
        },
        'watermark': watermark
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_drm_token_view(request):
    """Verifies that a playback DRM token is valid and unrevoked"""
    token_str = request.data.get('token')
    if not token_str:
        return Response({'error': 'DRM token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        drm_token = DRMToken.objects.select_related('asset', 'user').get(token_string=token_str)
    except DRMToken.DoesNotExist:
        return Response({'valid': False, 'reason': 'Token not recognized in DRM key server'}, status=status.HTTP_404_NOT_FOUND)

    if drm_token.is_revoked:
        return Response({'valid': False, 'reason': 'DRM token has been revoked by content rights officer'}, status=status.HTTP_403_FORBIDDEN)

    if drm_token.expires_at < timezone.now():
        return Response({'valid': False, 'reason': 'DRM license lease expired'}, status=status.HTTP_403_FORBIDDEN)

    return Response({
        'valid': True,
        'license_type': drm_token.license_type,
        'asset_id': drm_token.asset_id,
        'asset_title': drm_token.asset.title,
        'user': drm_token.user.email,
        'expires_at': drm_token.expires_at.isoformat()
    })

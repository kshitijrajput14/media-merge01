from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'platform': 'MediaMerge - Integrated Media Asset Management and Streaming Platform',
        'version': '1.0.0',
        'status': 'ONLINE',
        'modules': [
            'Asset metadata management',
            'Search and retrieval',
            'Access control and permissions',
            'Asset versioning and history',
            'Contract and rights management',
            'Royalty calculation and distribution',
            'Sales data integration',
            'Reporting and analytics',
            'User registration and authentication',
            'Subscription management and billing',
            'Content streaming and DRM',
            'Recommendation engine and personalization'
        ],
        'endpoints': {
            'core': '/api/',
            'assets': '/api/assets/',
            'search': '/api/assets/search/',
            'rights': '/api/rights/',
            'streaming': '/api/streaming/',
            'subscriptions': '/api/subscriptions/',
            'analytics': '/api/analytics/',
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/assets/', include('assets.urls')),
    path('api/rights/', include('rights.urls')),
    path('api/streaming/', include('streaming.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/analytics/', include('analytics.urls')),
]

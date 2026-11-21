import secrets
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Role, UserProfile
from .serializers import RoleSerializer, UserProfileSerializer, RegisterSerializer

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().select_related('role')
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        role_id = self.request.query_params.get('role_id')
        search = self.request.query_params.get('search')
        if role_id:
            qs = qs.filter(role_id=role_id)
        if search:
            qs = qs.filter(full_name__icontains=search) | qs.filter(email__icontains=search)
        return qs


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserProfile.objects.select_related('role').get(email__iexact=email)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': 'User account is deactivated'}, status=status.HTTP_403_FORBIDDEN)

    token = f"mm_token_{secrets.token_hex(24)}"
    return Response({
        'token': token,
        'user': UserProfileSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = f"mm_token_{secrets.token_hex(24)}"
        return Response({
            'message': 'User registered successfully',
            'token': token,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from .models import DRMPolicy, StreamingSession, DRMToken

class DRMPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = DRMPolicy
        fields = '__all__'


class StreamingSessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    asset_title = serializers.CharField(source='asset.title', read_only=True)

    class Meta:
        model = StreamingSession
        fields = '__all__'


class DRMTokenSerializer(serializers.ModelSerializer):
    asset_title = serializers.CharField(source='asset.title', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = DRMToken
        fields = '__all__'

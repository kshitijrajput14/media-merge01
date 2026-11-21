from rest_framework import serializers
from .models import Role, UserProfile

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user_id', 'role', 'role_name', 'full_name', 'email', 'phone_number', 'city', 'state', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UserProfile
        fields = ['user_id', 'role', 'full_name', 'email', 'password', 'phone_number', 'city', 'state']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(raw_password)
        user.save()
        return user
